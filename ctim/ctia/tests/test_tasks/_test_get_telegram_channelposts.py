import datetime
import logging
from unittest.mock import AsyncMock, Mock, patch

import pytest
from django.test import TestCase

from ctim.ctia.tasks.get_telegram_channelposts import get_telegram_channelposts

logger = logging.getLogger(__name__)


class MockMessage:
    def __init__(self):
        self.id = 12345  # Mock message_id
        self.text = "Sample message text"
        self.date = datetime.datetime.now()  # Mock date
        self.views = 10
        self.forwards = 5
        self.media = None  # or mock media object


class AsyncIterableMock:
    def __init__(self, items):
        self.items = items
        logger.info("\n____\nAsyncIterableMock initialized with items: \n%s\n____\n", items)

    async def __aiter__(self):
        logger.info("\n____\nStarting async iteration\n____\n")
        for item in self.items:
            yield item


async def simple_async_gen():
    logger.info("\n____\nStarting async iteration\n____\n")
    yield MockMessage()
    yield MockMessage()


@pytest.mark.django_db
class TestGetTelegramChannelPosts(TestCase):
    @patch("telethon.TelegramClient")
    async def test_get_telegram_channelposts_successful(self, mock_telegram_client):
        mock_client_instance = Mock()
        mock_telegram_client.return_value = mock_client_instance

        # Mock asynchronous methods with AsyncMock
        mock_client_instance.connect = AsyncMock()
        mock_client_instance.connect.return_value = None
        print(mock_client_instance.connect)  # Should show an AsyncMock object
        mock_client_instance.disconnect = AsyncMock(return_value=None)
        mock_client_instance.is_user_authorized = AsyncMock(return_value=True)
        mock_client_instance.get_entity = AsyncMock()

        # Set iter_messages to return AsyncIterableMock
        mock_client_instance.iter_messages.return_value = AsyncIterableMock([MockMessage(), MockMessage()])

        # Assertions
        mock_client_instance.connect.assert_awaited_once()
        mock_client_instance.is_user_authorized.assert_awaited_once()
        mock_client_instance.get_entity.assert_awaited_once_with("test_channel")
        mock_client_instance.iter_messages.assert_awaited_once()

        # Ensure the mock client instance is disconnected
        mock_client_instance.disconnect.assert_awaited_once()

    @patch("ctim.ctia.tasks.get_telegram_channelposts.TelegramClient")
    async def test_get_telegram_channelposts_handle_exception(self, mock_telegram_client):
        mock_client_instance = AsyncMock()
        mock_telegram_client.return_value = mock_client_instance
        mock_client_instance.connect.side_effect = Exception("Connection error")

        # Run the task and expect it to handle the exception
        with self.assertLogs("ctim.ctia.tasks.get_telegram_channelposts", level="ERROR") as log:
            await get_telegram_channelposts("test_channel")

        # Assertions
        self.assertIn("An unexpected error occurred: Connection error", log.output[0])

        # Ensure the mock client instance is disconnected
        mock_client_instance.disconnect.assert_awaited_once()
