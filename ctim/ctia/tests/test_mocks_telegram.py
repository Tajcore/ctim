# ctim/ctia/tests/test_mocks_telegram.py
from unittest import mock
from unittest.mock import AsyncMock, Mock

from django.db.models.base import ModelState
from django.db.utils import IntegrityError
from telethon import TelegramClient

from ctim.ctia.models.telegram import Channel


def get_mock_entity(title="mocked_entity_title"):
    mock_entity = mock.Mock()
    mock_entity.title = title
    return mock_entity


def get_mock_telegram_client(connected=True, mock_entity=None):
    if not mock_entity:
        mock_entity = get_mock_entity("mocled_entity_from_client")

    mock_client = mock.Mock(spec=TelegramClient)
    mock_client.connect = AsyncMock(return_value=connected)
    mock_client.is_user_authorized = AsyncMock(return_value=connected)
    mock_client.get_entity = AsyncMock(return_value=mock_entity)
    mock_client.disconnect = AsyncMock(return_value=True)
    mock_client.iter_messages = AsyncMock(return_value=iter([get_mock_channel_post()]))

    return mock_client


def get_mock_channel(name="mocked_channel", is_being_processed=False, last_processed_message_id=123):
    mock_channel = mock.create_autospec(Channel, instance=True)
    mock_channel.name = name
    mock_channel.is_being_processed = is_being_processed
    mock_channel.last_processed_message_id_async = AsyncMock(return_value=last_processed_message_id)
    mock_channel._state = ModelState()
    mock_channel.objects = Mock()
    mock_channel.objects.get_or_create = Mock(return_value=(mock_channel, True))
    return mock_channel


def get_mock_channel_post(message_id=1, content="Sample content"):
    mock_post = mock.Mock()
    mock_post.message_id = message_id
    mock_post.content = content
    return mock_post


def get_mock_failed_channel_post(error_message="Integrity error"):
    mock_failed_post = mock.Mock()
    mock_failed_post.error_message = error_message
    return mock_failed_post


def get_mock_telegram_api_response(error=None):
    if error:
        return AsyncMock(side_effect=error)
    return AsyncMock(return_value="Sample response")


def get_mock_celery_task(name="mock_task"):
    mock_task = mock.Mock()
    mock_task.name = name
    return mock_task


def get_mock_async_db_operation(success=True, exception=None):
    if not success:
        return AsyncMock(side_effect=exception)
    return AsyncMock(return_value="DB operation successful")


def get_mock_posts_batch(size=10):
    return [get_mock_channel_post(message_id=i) for i in range(size)]


def get_mock_logger():
    mock_logger = mock.Mock()
    mock_logger.error = mock.Mock()
    mock_logger.info = mock.Mock()
    mock_logger.debug = mock.Mock()
    return mock_logger


def get_mock_fetch_telegram_posts(posts_batch, min_id=123):
    async def mock_fetch_posts(client, entity, min_id):
        for post in posts_batch:
            yield post

    return AsyncMock(side_effect=mock_fetch_posts)


def get_mock_bulk_create(success=True, exception=None):
    async def mock_bulk_create(posts):
        if not success:
            raise IntegrityError(exception)

    return AsyncMock(side_effect=mock_bulk_create)


def get_mock_log_and_handle_failed_posts():
    mock_function = AsyncMock()
    return mock_function
