from aiogram import Router
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

campaign_create_router = Router()

class CreateCampaignStates(StatesGroup):
    enter_name = State()

# Я так предполагаю мы эти данные будем фетчить из бд через бекенд но я не знаю 
# как это написать щас поэтому вот так вот.
CAMPAIGN = [
    {"id": 1, "name": "Существующая кампания 1"},
    {"id": 2, "name": "Существующая кампания 2"},
]

async def on_create_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await callback.message.answer("Создание новой кампании...")


async def on_select_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):

    campaign_id = int(item_id)
    await callback.answer(f"Выбрана кампания {campaign_id}")


def get_campaigns_keyboard():

    buttons = []
    for campaign in CAMPAIGN:
        buttons.append(Button(
            Const(f"{campaign['name']}"),
            id=str(campaign["id"]),
            on_click=on_select_campaign,
        ))
    return Column(*buttons)


create_campaign_dialog = Dialog(
    Window(
        Const("**Главное меню**\n\nВыберите действие:"),
        Button(Const("Создать кампанию"), id="create", on_click=on_create_campaign),
        Const("\nВаши кампании:"),
        get_campaigns_keyboard(),
        state=CreateCampaignStates.enter_name,
    )
)
