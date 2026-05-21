import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from db.engine import engine
from db.models import Base
from bot.handlers import router as bot_router
from services.monitor import start_monitoring

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger("MainEntryPoint")


async def main() -> None:
    load_dotenv()
    logger.info("Initializing system startup.")
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        logger.critical("BOT_TOKEN is missing in environment variables! Process aborted.")
        sys.exit("Error: BOT_TOKEN not found.")

    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(bot_router)

    print("Checking and creating tables in a database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Checking and creating tables done")

    await bot.delete_webhook(drop_pending_updates=True)

    asyncio.create_task(start_monitoring(bot))

    logger.info("Telegram Bot successfully polished and starting polling loop.")
    print("The bot has launched and is starting to poll Telegram servers")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("System received shutdown signal. Bot stopped down cleanly.")