# ctim/ctia/tasks/get_telegram_channelposts.py
import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from billiard.exceptions import SoftTimeLimitExceeded
from celery import shared_task
from django.conf import settings
from django.db import IntegrityError
from telethon import TelegramClient
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    FloodWaitError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    UsernameInvalidError,
)

from ctim.ctia.models.telegram import Channel, ChannelPost, FailedChannelPost

logger = logging.getLogger(__name__)


@shared_task(name="get_telegram_channelposts", soft_time_limit=600)
def get_telegram_channelposts(channel_name):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_get_telegram_channelposts(channel_name))
    except SoftTimeLimitExceeded:
        logger.error("The task exceeded the soft_time_limit")
    except Exception as e:
        logger.error("An error occurred in get_telegram_channelposts: %s", e, exc_info=True)
        # Re-raise if you want Celery to handle the exception (e.g., retries)
        raise
    finally:
        loop.close()


async def create_telegram_client(telegram_phone, api_id, api_hash):
    client = TelegramClient(telegram_phone, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        raise Exception("Telegram client is not authorized")
    return client


async def get_telegram_entity(client, channel_name):
    return await client.get_entity(channel_name)


async def fetch_telegram_posts(client, entity, min_id):
    """
    Fetch posts from a Telegram channel starting from a given message ID.
    Returns an asynchronous iterator of posts.
    """
    return client.iter_messages(entity, min_id=min_id)


async def process_channel_posts(client, entity, channel, batch_size):
    posts_batch = []
    min_id = await channel.last_processed_message_id_async()

    async for post in await fetch_telegram_posts(client, entity, min_id):
        logger.debug("processing message: %s from channel %s", post.id, channel)
        media_data = None
        # if post.media:
        #    logger.debug("downloading media for post id: %s", post.id)
        #    media_path = os.path.join("path_to_media_folder", f"media_{post.id}")
        #    await post.download_media(file=media_path)
        #    media_data = {"path": media_path}

        channel_post = ChannelPost(
            channel=channel,
            message_id=post.id,
            content=post.text or "",
            date_posted=post.date,
            views=post.views or 0,
            forwards=post.forwards or 0,
            media_json=media_data,
        )
        posts_batch.append(channel_post)

        if len(posts_batch) >= batch_size:
            try:
                logger.debug("Saving batch, sized: %s", len(posts_batch))
                await sync_to_async(ChannelPost.objects.bulk_create)(posts_batch)
            except IntegrityError as e:
                await log_and_handle_failed_posts(e, posts_batch)
            posts_batch = []

    if posts_batch:
        logger.debug("Handling the last partial batch, sized: %s", len(posts_batch))
        try:
            await sync_to_async(ChannelPost.objects.bulk_create)(posts_batch)
        except IntegrityError as e:
            await log_and_handle_failed_posts(e, posts_batch)


async def async_get_telegram_channelposts(channel_name):
    channel = None
    created = None

    try:
        logger.info("Connecting to Telegram")
        client = await create_telegram_client(
            settings.TELEGRAM_PHONE, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH
        )
        logger.info("Connected to Telegram")

        entity = await get_telegram_entity(client, channel_name)
        channel, created = await sync_to_async(Channel.objects.get_or_create)(
            name=entity.title, url=f"https://t.me/{channel_name}"
        )

        logger.debug("Channel in DB: %s", channel)
    except FloodWaitError as e:
        logger.error("Rate limit exceeded, try again after %s seconds.", e.seconds)
    except (
        SessionPasswordNeededError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        ChannelPrivateError,
        ChannelInvalidError,
        UsernameInvalidError,
    ) as e:
        logger.error("Telegram API error: %s", e)

    logger.info("Checking if channel is being processed")

    if not created and channel.is_being_processed:
        logger.info("Channel is currently being processed by another instance. Exiting task...")
        try:
            await client.disconnect()
        except Exception as e:
            logger.error("Error disconnecting client: %s", e)
        finally:
            return

    try:
        logger.info("Processing channel")
        channel.is_being_processed = True
        await sync_to_async(channel.save)()

        await process_channel_posts(client, entity, channel, settings.TELEGRAM_BATCH_SIZE)

        logger.info("Scraped messages from %s completed.", channel_name)

    except Exception as e:
        logger.exception("An unexpected error occurred: %s", e)
    finally:
        if channel:
            logger.debug("reverting is_being_processed flag to false for channel: %s", channel)
            channel.is_being_processed = False
            await sync_to_async(channel.save)()
        if client:
            await client.disconnect()

    return "Test completed"


async def log_and_handle_failed_posts(error, batch):
    logger.error("Failed to insert posts due to IntegrityError: %s", error)
    # Get message IDs from the batch
    message_ids = [post.message_id for post in batch]

    # Define an asynchronous function to get existing IDs
    @sync_to_async
    def get_existing_ids():
        return set(ChannelPost.objects.filter(message_id__in=message_ids).values_list("message_id", flat=True))

    # Call the asynchronous function
    existing_ids = await get_existing_ids()

    logger.debug("saving failed posts in the FailedChannelPost object")
    failed_posts = [post for post in batch if post.message_id in existing_ids]
    logger.debug("failed_posts: %s", failed_posts)
    for post in failed_posts:
        logger.debug("converting %s to a dict", post)

        # Serialize only if not already a string
        media_json = json.dumps(post.media) if isinstance(post.media, dict) else post.media
        entities_json = json.dumps(post.entities) if isinstance(post.entities, dict) else post.entities

        # Check types and log them
        logger.debug("JSON of post.media: %s, post.entities: %s", media_json, entities_json)

        try:
            post_data = {
                "channel_id": post.channel_id,  # Assuming you want to store the ID of the channel
                "message_id": post.message_id,
                "content": post.content,
                "date_posted": post.date_posted.isoformat() if post.date_posted else None,
                "edit_date": post.edit_date.isoformat() if post.edit_date else None,
                "views": post.views,
                "forwards": post.forwards,
                "reply_count": post.reply_count,
                "media_json": media_json,
                "entities_json": entities_json,
                "message_url": post.message_url,
            }

            logger.debug(
                "channel: %s, saving failed post %s in the FailedChannelPost object", post.channel_id, post.message_id
            )

            post_data_json = json.dumps(post_data)
            logger.debug("Serialized post data: %s", post_data_json)

            await sync_to_async(FailedChannelPost.objects.create)(
                channel_post_data=post_data_json, error_message=str(error)
            )

        except Exception as e:
            logger.error("Failed to save failed channel post: %s because: %s", post.message_id, e)
