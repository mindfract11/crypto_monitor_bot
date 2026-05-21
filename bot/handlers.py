from sqlalchemy import select
from aiogram import Router, types
from db.engine import AsyncSessionLocal
from services.api_client import get_crypto_price

from db.models import User
from aiogram.filters import Command
from aiogram.types import Message
from db.models import Subscription
router = Router()

@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message) -> None:
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.answer(
                " Format error! Use: /subscribe [ticker] [target_price]\nExample: /subscribe bitcoin 75000")
            return

        ticker = args[1].lower()
        target_price = float(args[2])

        new_subscription = Subscription(
            user_id=message.from_user.id,
            ticker=ticker,
            target_price=target_price
        )

        async with AsyncSessionLocal() as db:
            db.add(new_subscription)
            await db.commit()

        await message.answer(
            f" Successfully subscribed! I will notify you when {ticker.upper()} hits ${target_price:,}")

    except ValueError:
        await message.answer(" Error! Price must be a valid number.")
    except Exception as e:
        await message.answer(" Something went wrong while saving your subscription.")
@router.message(Command("start"))
async def start(message: types.Message):
    async with AsyncSessionLocal() as db:
        query = select(User).where(User.id == message.from_user.id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            new_user = User(
                id=message.from_user.id,
                username = message.from_user.username

            )
            db.add(new_user)
            await db.commit()

            await message.answer("Welcome! You have successfully registered.")
        else:
            await message.answer(f"Nice to see you again, {user.username}!")
@router.message(Command("crypto"))
async def cmd_crypto(message: types.Message):
    processing_msg = await message.answer("I get the current Bitcoin rate...")

    try:
        price = await get_crypto_price("bitcoin")
        await message.answer(f" Current value Bitcoin: ${price:,}")
    except Exception as e:
        await message.answer("Sorry, we couldn't get the course. Please try again later.")
    finally:
        await processing_msg.delete()

