from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup


start_menu_router = Router()

CAMPAIGNS = [
    {"id": 1, "name": "Существующая кампания 1"},
    {"id": 2, "name": "Существующая кампания 2"},
]


class MainMenuStates(StatesGroup):
    main = State()


async def on_create_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    from .create_campaign import CreateCampaignStates
    await dialog_manager.start(CreateCampaignStates.enter_name)


async def on_select_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    campaign_id = button.widget_id
    campaign_name = next((c["name"] for c in CAMPAIGNS if str(c["id"]) == campaign_id), "Неизвестная")
    await callback.answer(f"Выбрана кампания: {campaign_name}")


# ! Предполагается что мы будем фетчить кампании из ДБ
def get_campaigns_keyboard():
    buttons = []
    for campaign in CAMPAIGNS:
        buttons.append(
            Button(
                Const(f"{campaign['name']}"),
                id=str(campaign["id"]),
                on_click=on_select_campaign,
            )
        )
    return Column(*buttons)


# * Диалог Главного / Стартового Меню
start_menu_dialog = Dialog(
    Window(
        Const("**Главное меню DnD бота**\n\nВыберите кампанию:"),
        Button(
            Const("Cоздать новую кампанию"),
            id="create_campaign",
            on_click=on_create_campaign,
        ),        
        Const("\nСуществующие кампании:"),
        get_campaigns_keyboard(),
        state=MainMenuStates.main,
    )
)

@start_menu_router.message(Command("start"))
@start_menu_router.message(Command("menu"))
async def cmd_main_menu(message: types.Message, dialog_manager: DialogManager):
    
    await dialog_manager.start(MainMenuStates.main)