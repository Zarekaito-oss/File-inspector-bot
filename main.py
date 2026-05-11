import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

from handlers import stripper, general

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN is not set. Add it to your .env file.")
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(general.router)
    dp.include_router(stripper.router)

    logger.info("\U0001f6e1\ufe0f  Metadata Stripper Bot is starting...")
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
