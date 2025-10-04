import asyncio
import logging
import os

import handlers

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs


TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise Exception("Null token provided")

async def main() -> None:
    dp = Dispatcher()

    # сюда добавляются обработчики
    dp.include_routers(
        handlers.connection_test_router,
        handlers.start_menu_router,
        handlers.start_menu_dialog,
        handlers.create_campaign_router,
        handlers.create_campaign_dialog,
    )

    setup_dialogs(dp)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
