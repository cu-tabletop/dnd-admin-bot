from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput

from .campaign_interaction import CampaignInteractionStates
from .start_menu import CAMPAIGNS

add_master_router = Router()


class AddMasterStates(StatesGroup):
    main = State()


async def on_add_master(message: Message, widget: TextInput,
                       dialog_manager: DialogManager, text: str):
    
    dialog_manager.dialog_data["master_id"] = text
    await dialog_manager.start(CampaignInteractionStates.main)

    # /api/campaign/{id}/add/master
    await message.answer(f"{text} теперь ГМ этой кампании")


async def get_data(dialog_manager: DialogManager, **kwargs):

    return {
        "campaign_name": CAMPAIGNS[0]["name"],
        "icon": CAMPAIGNS[0]["icon"]
    }


add_master_dialog = Dialog(
    Window(
        Format("**Добавление гейм-мастера к кампании *{campaign_name}"),
        TextInput(
            id="master_id_input",
            on_success=on_add_master
        ),
        Cancel(Const("Отмена")),
    state=AddMasterStates.main,
    getter=get_data,
    )
)