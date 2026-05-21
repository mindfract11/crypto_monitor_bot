import asyncio
import logging
from aiogram import Bot
from sqlalchemy import select, delete

from db.engine import AsyncSessionLocal
from db.models import Subscription
from services.api_client import get_crypto_price

logger = logging.getLogger("BackgroundMonitor")


async def start_monitoring(bot: Bot) -> None:
    logger.info("Background monitoring task has been successfully initialized.")

    while True:
        try:
            logger.info("Starting a new crypto price check cycle...")

            btc_price = await get_crypto_price("bitcoin")

            if btc_price is None:
                logger.warning("Failed to fetch price from CoinGecko. Skipping this iteration.")
                await asyncio.sleep(1200)
                continue

            async with AsyncSessionLocal() as db:
                query = select(Subscription)
                result = await db.execute(query)
                subscriptions = result.scalars().all()

                triggered_ids = []

                for sub in subscriptions:
                    try:

                        if btc_price >= sub.target_price:
                            await bot.send_message(
                                chat_id=sub.user_id,
                                text=f"{sub.ticker.upper()} has reached your target price of ${sub.target_price:,}! Current price: ${btc_price:,}"
                            )

                            triggered_ids.append(sub.id)

                    except Exception as send_error:
                        logger.error(f"Failed to send alert to user {sub.user_id}: {send_error}")
                if triggered_ids:
                    delete_query = delete(Subscription).where(Subscription.id.in_(triggered_ids))
                    await db.execute(delete_query)
                    await db.commit()
                    logger.info(f"Successfully removed {len(triggered_ids)} triggered subscriptions from DB.")

        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")

        await asyncio.sleep(1200)