import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config.settings import settings, setup_logging
from handlers.start import router as start_router
from dialogs.character_management import character_management_dialog

async def main():
    setup_logging(settings.LOG_LEVEL)
    
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрируем роутеры и диалоги
    dp.include_router(start_router)
    dp.include_router(character_management_dialog)
    setup_dialogs(dp)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    