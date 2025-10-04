from aiogram import Router
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.api.entities import MediaAttachment

from .start_menu import MainMenuStates
from ..services import constants
create_campaign_router = Router()


class CreateCampaignStates(StatesGroup):
    enter_name = State()
    enter_description = State()
    enter_icon = State()
    confirm = State()


async def on_name_entered(message: Message, widget: TextInput, 
                         dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data["name"] = text
    await dialog_manager.next()


async def on_description_entered(message: Message, widget: TextInput,
                                dialog_manager: DialogManager, text: str):

    dialog_manager.dialog_data["description"] = text
    await dialog_manager.next()


async def on_icon_entered(message: Message, widget: MessageInput, dialog_manager: DialogManager, **kwargs):

    if message.photo:

        photo = message.photo[-1]
        dialog_manager.dialog_data["icon_file_id"] = photo.file_id

    else:

        dialog_manager.dialog_data["icon_file_id"] = constants.DEFAULT_ICON_ID
    
    await dialog_manager.next()


async def on_skip_description(callback: CallbackQuery, button: Button,
                            dialog_manager: DialogManager):

    dialog_manager.dialog_data["description"] = ""
    await dialog_manager.next()


async def on_skip_icon(callback: CallbackQuery, button: Button,
                      dialog_manager: DialogManager):

    dialog_manager.dialog_data["icon"] = ""
    await dialog_manager.next()


async def on_confirm(callback: CallbackQuery, button: Button,
                    dialog_manager: DialogManager):

    campaign_data = dialog_manager.dialog_data
    
    # Здесь будет вызов API для создания кампании
    # response = requests.post('/api/campaign/create/', json=campaign_data)

    # POST /api/campaign/create/ требует 
    # telegram_id - длинное такое число, уникальный айдишник в тг
    # title - название новой кампании (до 256 символов)
    # description - описание (до 1024 символов) (опционально)
    # icon - иконка в base64 (опционально)
    
    await callback.message.answer(
        f"Кампания '{campaign_data['name']}' создана!\n"
        f"Описание: {campaign_data.get('description', 'не указано')}\n"
        f"Иконка: {campaign_data.get('icon', 'не указана')}"
    )
    
    await dialog_manager.start(MainMenuStates.main)


async def on_cancel(callback: CallbackQuery, button: Button,
                   dialog_manager: DialogManager):

    await callback.message.answer("Создание кампании отменено")
    await dialog_manager.start(MainMenuStates.main)


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):

    return {
        "name": dialog_manager.dialog_data.get("name", ""),
        "description": dialog_manager.dialog_data.get("description", "не указано"),
        "icon": dialog_manager.dialog_data.get("icon")
    }



create_campaign_dialog = Dialog(
    Window(
        Const("**Создание новой кампании**\n\nВведите название кампании:"),
        TextInput(
            id="name_input",
            on_success=on_name_entered,
        ),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.enter_name,
    ),
    Window(
        Const("**Введите описание кампании**\n\nМожно пропустить:"),
        TextInput(
            id="description_input", 
            on_success=on_description_entered,
        ),
        Row(
            Button(Const("Пропустить"), id="skip_desc", on_click=on_skip_description),
            Back(Const("Назад")),
        ),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.enter_description,
    ),
    Window(
        Const("**Введите иконку для кампании**\n\nМожно пропустить:"),
        MessageInput(
            func=on_icon_entered,
            content_types=ContentType.PHOTO
        ),
        Row(
            Button(Const("Пропустить"), id="skip_icon", on_click=on_skip_icon),
            Back(Const("Назад")),
        ),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.enter_icon,
    ),
    Window(
        DynamicMedia('icon'),
        Format(
            "**Подтверждение создания**\n\n"
            "Название: {name}\n "
            "Описание: {description}\n"
            "Создать кампанию?"
        ),
        Button(Const("Создать"), id="confirm", on_click=on_confirm),
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
        state=CreateCampaignStates.confirm,
        getter=get_confirm_data,
    )
)