import asyncio
import logging
import os

import handlers

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise Exception("Null token provided")

async def main() -> None:
    dp = Dispatcher()

    # сюда добавляются обработчики
    dp.include_routers(
        handlers.start_router,
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
