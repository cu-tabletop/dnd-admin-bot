from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Column
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

# Создаем router для диалога
router = Router()

# Состояния для главного меню
class MainMenuStates(StatesGroup):
    main = State()

# Заглушка данных о кампаниях
SAMPLE_CAMPAIGNS = [
    {"id": 1, "name": "Существующая кампания 1"},
    {"id": 2, "name": "Существующая кампания 2"},
]

# Обработчики кнопок
async def on_create_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик создания новой кампании"""
    await callback.answer("Создание новой кампании...")

async def on_select_campaign(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик выбора существующей кампании"""
    campaign_id = button.widget_id
    campaign_name = next((c["name"] for c in SAMPLE_CAMPAIGNS if str(c["id"]) == campaign_id), "Неизвестная")
    await callback.answer(f"Выбрана кампания: {campaign_name}")

# Создаем клавиатуру
def get_campaigns_keyboard():
    buttons = []
    for campaign in SAMPLE_CAMPAIGNS:
        buttons.append(
            Button(
                Const(f"{campaign['name']}"),
                id=str(campaign["id"]),  # ID кнопки
                on_click=on_select_campaign,
            )
        )
    return Column(*buttons)

# Диалог главного меню
main_menu_dialog = Dialog(
    Window(
        Const("**Главное меню DnD бота**\n\nВыберите кампанию:"),
        
        # Кнопка создания новой кампании
        Button(
            Const("Cоздать новую кампанию"),
            id="create_campaign",
            on_click=on_create_campaign,
        ),
        
        Const("\nСуществующие кампании:"),
        
        # Список существующих кампаний
        get_campaigns_keyboard(),
        
        state=MainMenuStates.main,
    )
)

# Обычный хендлер для команды /start
@router.message(Command("start"))
@router.message(Command("menu"))
async def cmd_main_menu(message: types.Message, dialog_manager: DialogManager):
    """Запуск главного меню по команде"""
    await dialog_manager.start(MainMenuStates.main)