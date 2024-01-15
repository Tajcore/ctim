"""
TestCreateTelegramClient.test_create_telegram_client_authorized:
    Tests if create_telegram_client function correctly creates and
    returns an authorized Telegram client.
TestCreateTelegramClient.test_create_telegram_client_not_authorized:
    Ensures create_telegram_client raises an exception when the Telegram
    client is not authorized.
TestGetTelegramEntity.test_get_telegram_entity:
    Checks if get_telegram_entity function correctly retrieves a Telegram
    entity and returns it.
"""
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from django.conf import settings

from ctim.ctia.tasks.get_telegram_channelposts import (
    async_get_telegram_channelposts,
    create_telegram_client,
    get_telegram_entity,
    process_channel_posts,
)
from ctim.ctia.tests.test_mocks_telegram import (
    get_mock_channel,
    get_mock_channel_post,
    get_mock_entity,
    get_mock_telegram_client,
)


class AsyncIteratorMock:
    def __init__(self, items):
        self._items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._items:
            raise StopAsyncIteration
        return self._items.pop(0)


class TestCreateTelegramClient(unittest.TestCase):
    @patch("ctim.ctia.tasks.get_telegram_channelposts.TelegramClient")
    def test_create_telegram_client_authorized(self, mock_telegram_client):
        async def async_test():
            # Setup mock
            mock_client = get_mock_telegram_client(connected=True)
            mock_telegram_client.return_value = mock_client

            # Call the function
            client = await create_telegram_client("phone", "api_id", "api_hash")

            # Assertions
            mock_telegram_client.assert_called_with("phone", "api_id", "api_hash")
            mock_client.connect.assert_awaited_once()
            self.assertIsNotNone(client)

        asyncio.run(async_test())

    @patch("ctim.ctia.tasks.get_telegram_channelposts.TelegramClient")
    def test_create_telegram_client_not_authorized(self, mock_telegram_client):
        async def async_test():
            # Setup mock
            mock_client = get_mock_telegram_client(connected=False)
            mock_telegram_client.return_value = mock_client

            # Test and Assertions
            with self.assertRaises(Exception):
                await create_telegram_client("phone", "api_id", "api_hash")

        asyncio.run(async_test())


class TestGetTelegramEntity(unittest.TestCase):
    @patch("ctim.ctia.tasks.get_telegram_channelposts.TelegramClient")
    def test_get_telegram_entity(self, mock_telegram_client):
        async def async_test():
            # Setup mock
            entity_name = "test_channel"
            mock_entity = get_mock_entity(title=entity_name)
            mock_client = get_mock_telegram_client(connected=True, mock_entity=mock_entity)

            # Call the function
            result = await get_telegram_entity(mock_client, entity_name)

            # Assertions
            mock_client.get_entity.assert_awaited_with(entity_name)
            self.assertEqual(result, mock_entity)

        asyncio.run(async_test())


class TestProcessChannelPosts(unittest.TestCase):
    @patch("ctim.ctia.tasks.get_telegram_channelposts.create_telegram_client")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.get_telegram_entity")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.sync_to_async")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.fetch_telegram_posts")
    def test_process_channel_posts(
        self, mock_fetch_telegram_posts, mock_sync_to_async, mock_get_telegram_entity, mock_create_telegram_client
    ):
        async def async_test():
            # Setup mocks
            entity_name = "test_channel"
            mock_entity = get_mock_entity(title=entity_name)
            mock_client = get_mock_telegram_client(connected=True, mock_entity=mock_entity)
            mock_channel = get_mock_channel()
            mock_sync_to_async.return_value = AsyncMock()  # Mock database operations
            mock_create_telegram_client.return_value = mock_client
            mock_get_telegram_entity.return_value = mock_entity

            # Setup mock for fetch_telegram_posts to return an AsyncIteratorMock
            mock_fetch_telegram_posts.return_value = AsyncIteratorMock([AsyncMock(), AsyncMock()])

            # Call the function with all required parameters
            await process_channel_posts(mock_client, mock_entity, mock_channel, 10)

            # Assertions
            min_id = await mock_channel.last_processed_message_id_async()
            mock_fetch_telegram_posts.assert_called_with(mock_client, mock_entity, min_id)
            mock_sync_to_async.assert_called()  # Verify database interactions

        asyncio.run(async_test())


class TestAsyncGetTelegramChannelPosts(unittest.TestCase):
    @patch("ctim.ctia.tasks.get_telegram_channelposts.create_telegram_client")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.get_telegram_entity")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.process_channel_posts")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.Channel")
    @patch("ctim.ctia.tasks.get_telegram_channelposts.ChannelPost")
    def test_successful_execution(
        self,
        mock_channel_post,
        mock_channel,
        mock_process_channel_posts,
        mock_get_telegram_entity,
        mock_create_telegram_client,
    ):
        async def async_test():
            # Setup mocks for ChannelPost
            mock_channel_post.side_effect = lambda **kwargs: get_mock_channel_post(**kwargs)

            # Setup mock Channel with the get_mock_channel function
            mock_channel_instance = get_mock_channel()
            mock_channel.objects.get_or_create = AsyncMock(return_value=(mock_channel_instance, True))

            # Setup other mocks
            mock_client = get_mock_telegram_client(connected=True)
            mock_entity = get_mock_entity(title="Test Channel")
            mock_create_telegram_client.return_value = mock_client
            mock_get_telegram_entity.return_value = mock_entity
            mock_process_channel_posts.return_value = None

            # Execute the test
            result = await async_get_telegram_channelposts("Test Channel")

            # Assertions
            mock_create_telegram_client.assert_awaited_once_with(
                settings.TELEGRAM_PHONE, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH
            )
            mock_get_telegram_entity.assert_awaited_once_with(mock_client, "Test Channel")
            mock_process_channel_posts.assert_awaited_once_with(
                mock_client, mock_entity, mock_channel_instance, settings.TELEGRAM_BATCH_SIZE
            )
            self.assertEqual(result, "Test completed")

        asyncio.run(async_test())


# TestAsyncGetTelegramChannelPosts.test_successful_execution
# TestAsyncGetTelegramChannelPosts.test_flood_wait_error_handling
# TestAsyncGetTelegramChannelPosts.test_other_telegram_api_errors
# TestDatabaseOperationsProcessChannelPosts.test_batch_saving_successful
# TestDatabaseOperationsProcessChannelPosts.test_handling_integrity_error_on_batch_save
# TestExceptionHandlingGetTelegramChannelPosts.test_soft_time_limit_exceeded_handling
# TestTelegramClientConnection.test_client_connection_failure
# TestTelegramClientConnection.test_client_authorization_issues
# TestTelegramEntityRetrieval.test_entity_retrieval_failure
# TestAsyncGetTelegramChannelPosts.test_channel_already_being_processed
# TestExceptionHandlingGetTelegramChannelPosts.test_general_exception_handling
# TestDatabaseOperationsProcessChannelPosts.test_handling_last_partial_batch
# TestEdgeCasesAsyncGetTelegramChannelPosts.test_zero_posts_to_process
# TestEdgeCasesAsyncGetTelegramChannelPosts.test_exact_batch_size_posts
# TestErrorHandlingInBatches.test_handling_different_batch_sizes
# TestErrorHandlingInBatches.test_handling_last_partial_batch_errors
