from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from dialogs.states import CharacterManagementSG

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(CharacterManagementSG.company_selection, mode=StartMode.RESET_STACK)