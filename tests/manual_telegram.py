# Import necessary libraries
import asyncio
import logging

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Define the function to create a Telegram client
async def create_telegram_client(telegram_phone, api_id, api_hash):
    logger.debug("Creating Telegram client")
    client = TelegramClient(telegram_phone, api_id, api_hash)
    await client.connect()
    logger.debug("Connected to Telegram")

    if not await client.is_user_authorized():
        logger.debug("Client is not authorized, sending code request")
        await client.send_code_request(telegram_phone)
        code = input("Enter the code you received: ")
        try:
            await client.sign_in(telegram_phone, code)
        except SessionPasswordNeededError:
            password = input("Two-step verification enabled. Please enter your password: ")
            await client.sign_in(password=password)

    if not await client.is_user_authorized():
        logger.error("Telegram client is not authorized after sign-in attempt")
        raise Exception("Telegram client is not authorized")

    logger.debug("Client is authorized")
    return client


# Test the function interactively
async def test_create_telegram_client():
    telegram_phone = input("Enter your Telegram phone number: ")
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API Hash: ")

    try:
        await create_telegram_client(telegram_phone, api_id, api_hash)
        print("Client is authorized!")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


# Run the test
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_create_telegram_client())
