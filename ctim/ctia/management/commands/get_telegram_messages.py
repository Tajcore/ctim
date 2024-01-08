# ctim/ctia/management/commands/get_telegram_messages.py
import asyncio
import logging
import os
import traceback
from pprint import pformat

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    FloodWaitError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)
from telethon.sync import TelegramClient

from ctim.ctia.models.telegram import Channel, ChannelPost


class Command(BaseCommand):
    help = "Scrapes messages from a specified Telegram channel"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.verbosity = 1  # Default verbosity level

    def add_arguments(self, parser):
        parser.add_argument("channel_name", type=str, help="Telegram channel name (e.g. team_heroxx)")

    async def scrape_channel_content(self, channel_name, client):
        try:
            # Connect to the Telegram client
            await client.connect()

            # Check if the client is authorized, if not, then start the client
            if not await client.is_user_authorized():
                # For a user account
                await client.send_code_request(settings.TELEGRAM_PHONE)
                # You will need to manually enter the code or find a way to automate this
                code = input("Enter the code: ")
                await client.sign_in(settings.TELEGRAM_PHONE, code)

            entity = await client.get_entity(channel_name)
            channel, _ = await sync_to_async(Channel.objects.get_or_create)(
                name=entity.title, url=f"https://t.me/{channel_name}"
            )

            async for post in client.iter_messages(entity):
                self.logger.debug(f"\n_____\nPost: {post.id}, \nContent: {post.text}, \n")
                self.logger.debug(f"Full Post Object: {pformat(post.to_dict())}\n_____\n")

                # Create or update ChannelPost instead of Message
                channel_post, created = await sync_to_async(ChannelPost.objects.get_or_create)(
                    channel=channel,
                    message_id=post.id,
                    defaults={
                        "content": post.text or "",
                        "date_posted": post.date,
                        "views": post.views or 0,
                        "forwards": post.forwards or 0,
                        # Include other relevant fields from post.to_dict()
                    },
                )

                # Handle media if present
                if post.media and created:
                    media_path = os.path.join("path_to_media_folder", f"media_{post.id}")
                    await post.download_media(file=media_path)
                    # Update media_json or similar field in ChannelPost
                    media_data = {
                        "path": media_path,
                        # Add more media details if needed
                    }
                    channel_post.media_json = media_data
                    await sync_to_async(channel_post.save)()

                self.stdout.write(f"Scraped message {channel_post.message_id} from {channel_name}")

        except FloodWaitError as e:
            self.stdout.write(self.style.ERROR(f"Rate limit exceeded, try again after {e.seconds} seconds."))
        except (SessionPasswordNeededError, PhoneCodeInvalidError, PhoneCodeExpiredError) as e:
            self.stdout.write(self.style.ERROR(f"Authentication error: {e}"))
        except (ChannelPrivateError, ChannelInvalidError) as e:
            self.stdout.write(self.style.ERROR(f"Channel access error: {e}"))
        except Exception as e:
            if self.verbosity >= 3:
                # Print full traceback for high verbosity
                self.stdout.write(self.style.ERROR(f"An unexpected error occurred:\n{traceback.format_exc()}"))
            else:
                # Print only the exception message for lower verbosity
                self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
        finally:
            # Disconnect the client after the scraping is done
            await client.disconnect()

    def handle(self, *args, **kwargs):
        self.verbosity = kwargs.get("verbosity", 1)
        if self.verbosity == 3:  # Highest verbosity corresponds to DEBUG level
            logging.getLogger().setLevel(logging.DEBUG)
        channel_name = kwargs["channel_name"]
        self.stdout.write(self.style.SUCCESS(f"Starting to scrape {channel_name}..."))

        api_id = settings.TELEGRAM_API_ID
        api_hash = settings.TELEGRAM_API_HASH
        phone = settings.TELEGRAM_PHONE

        client = TelegramClient(phone, api_id, api_hash)

        asyncio.run(self.scrape_channel_content(channel_name, client))

        self.stdout.write(self.style.SUCCESS("Scraping completed."))
