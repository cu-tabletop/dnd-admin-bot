from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row

from .create_campaign import CreateCampaignStates
from .start_menu import CAMPAIGNS

campaign_interaction_router = Router()


class CampaignInteractionStates(StatesGroup):

    main = State()
    characters = State()
    add_admins = State()


async def on_cancel(callback: CallbackQuery, button: Button,
                   dialog_manager: DialogManager):

    from .start_menu import MainMenuStates
    await dialog_manager.start(MainMenuStates.main)


async def on_start_add_admin(message: Message, button: Button,
                       dialog_manager: DialogManager):
    from .add_admin import AddAdminStates
    await dialog_manager.start(AddAdminStates.main)



async def on_chars_transition(message: Message, button: Button,
                               dialog_manager: DialogManager):

    pass


async def get_panel_data(dialog_manager: DialogManager, **kwargs):

    return {
        "campaign_name": CAMPAIGNS[0]["name"],
        "icon": CAMPAIGNS[0]["icon"]
    }


campaign_interaction_dialog = Dialog(
    Window(
        DynamicMedia("icon"),
        Format(
            "Панель управления кампанией {campaign_name}\n"
        ),
        Button(
            Const("Персонажи"),
            id="characters",
            on_click=on_chars_transition,
        ),
        Button(
            Const("Пригласить другого ГМа"),
            id="invite_gm",
            on_click=on_start_add_admin,
        ),
        Row(
            Back(Const("Назад")),
            Cancel(Const("Отмена")),
        ),
        state=CampaignInteractionStates.main,
        getter=get_panel_data,
    )
)