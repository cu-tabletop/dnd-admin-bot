from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row, Group, Back, Cancel, Select
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram.types import Message, CallbackQuery
from functools import partial

from utils.logger import get_logger
from .states import CharacterManagementSG
from services.api_client import get_api_client
from .inventory_management import inventory_management_dialog

api_client = get_api_client()


# Хендлеры для клавиатур
async def on_company_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    manager.dialog_data["company_id"] = int(item_id)
    await manager.next()


async def on_character_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    manager.dialog_data["character_id"] = int(item_id)
    await manager.next()


# Геттеры для данных
async def get_companies(dialog_manager: DialogManager, **kwargs):
    companies = await api_client.get_companies()
    return {"companies": companies}


async def get_characters(dialog_manager: DialogManager, **kwargs):
    company_id = dialog_manager.dialog_data.get("company_id")
    characters = await api_client.get_company_characters(company_id)  # type: ignore
    return {"characters": characters}


async def get_character_data(dialog_manager: DialogManager, **kwargs):
    character_id = dialog_manager.dialog_data.get("character_id")
    character = await api_client.get_character(character_id)  # type: ignore
    return {"character": character}


# Окно выбора компании
company_window = Window(
    Const("🎯 Выберите компанию:"),
    Group(
        Select(
            Format("{item.name}"),
            id="company_select",
            item_id_getter=lambda x: x.id,
            items="companies",
            on_click=on_company_selected,
        ),
        width=2,
    ),
    Cancel(Const("❌ Отмена")),
    state=CharacterManagementSG.company_selection,
    getter=get_companies,
)

# Окно выбора персонажа
character_window = Window(
    Const("🧙 Выберите персонажа:"),
    Group(
        Select(
            Format("{item.name} (Ур. {item.level})"),
            id="character_select",
            item_id_getter=lambda x: x.id,
            items="characters",
            on_click=on_character_selected,
        ),
        width=1,
    ),
    Back(Const("⬅️ Назад")),
    Cancel(Const("❌ Отмена")),
    state=CharacterManagementSG.character_selection,
    getter=get_characters,
)


# Обработчики для меню персонажа
async def on_change_level(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(CharacterManagementSG.change_level)


async def on_change_rating(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(CharacterManagementSG.change_rating)


async def on_view_inventory(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.switch_to(CharacterManagementSG.view_inventory)


async def on_download_jpeg(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    character_id = manager.dialog_data.get("character_id")
    try:
        jpeg_data = await api_client.get_character_jpeg(character_id)  # type: ignore
        await callback.message.answer_document(  # type: ignore
            document=BufferedInputFile(
                jpeg_data, filename=f"character_{character_id}.jpg"
            )
        )
    except Exception:
        await callback.message.answer("❌ Ошибка при загрузке файла")  # type: ignore


async def on_change_rating_click(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    """Обработчик нажатия кнопки изменения рейтинга"""
    await manager.switch_to(CharacterManagementSG.change_rating)


async def on_quick_rating_change(
    callback: CallbackQuery, widget: Button, manager: DialogManager, item_id: str
):
    """Обработчик быстрого изменения рейтинга (+/- 1, 5, 10)"""
    try:
        character_id = manager.dialog_data.get("character_id", 0)
        current_character = await api_client.get_character(character_id)
        current_rating = current_character.rating

        change = int(item_id)
        new_rating = current_rating + change

        # Валидация
        if new_rating < 0:
            new_rating = 0
        if new_rating > 1000:
            new_rating = 1000

        # Обновление
        await api_client.update_character_rating(character_id, new_rating)

        # Показываем обновленные данные
        await manager.show(CharacterManagementSG.character_menu)  # type: ignore

    except Exception as e:
        logger = manager.middleware_data.get("logger", get_logger(__name__))
        logger.error(f"Error in quick rating change: {e}")
        await callback.answer("❌ Ошибка при изменении рейтинга")


async def on_rating_input(
    message: Message, widget: ManagedTextInput, manager: DialogManager, text: str
):
    """Обработчик ввода нового рейтинга"""
    try:
        rating = int(text)
        character_id = manager.dialog_data.get("character_id")

        # Валидация рейтинга
        if rating < 0:
            await message.answer("❌ Рейтинг не может быть отрицательным")
            return
        if rating > 1000:  # Пример ограничения
            await message.answer("❌ Рейтинг не может превышать 1000")
            return

        # Обновляем рейтинг через API
        await api_client.update_character_rating(character_id, rating)  # type: ignore

        await message.answer(f"✅ Рейтинг успешно изменен на {rating}")
        await manager.switch_to(CharacterManagementSG.character_menu)

    except ValueError:
        await message.answer("❌ Пожалуйста, введите целое число")
    except Exception as e:
        logger = manager.middleware_data.get("logger", get_logger(__name__))
        logger.error(f"Error updating rating: {e}")
        await message.answer("❌ Ошибка при обновлении рейтинга")


# окно для изменения рейтинга
rating_window = Window(
    Multi(
        Format("🏆 Изменение рейтинга для {character.name}"),
        Format("Текущий рейтинг: {character.rating}"),
        Const(""),
        Const("Введите новый рейтинг:"),
        sep="\n",
    ),
    TextInput(
        id="rating_input",
        on_success=on_rating_input,
    ),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, b, m: m.switch_to(CharacterManagementSG.character_menu),
    ),
    state=CharacterManagementSG.change_rating,
    getter=get_character_data,  # Используем существующий геттер
)

# Окно быстрого изменения рейтинга
quick_rating_window = Window(
    Multi(
        Format("🏆 Быстрое изменение рейтинга"),
        Format("Персонаж: {character.name}"),
        Format("Текущий рейтинг: {character.rating}"),
        Const(""),
        Const("Выберите изменение:"),
        sep="\n",
    ),
    Group(
        Row(
            Button(
                Const("+1"),
                id="rating_plus_1",
                on_click=partial(on_quick_rating_change, item_id="1"),
            ),
            Button(
                Const("+5"),
                id="rating_plus_5",
                on_click=partial(on_quick_rating_change, item_id="5"),
            ),
            Button(
                Const("+10"),
                id="rating_plus_10",
                on_click=partial(on_quick_rating_change, item_id="10"),
            ),
        ),
        Row(
            Button(
                Const("-1"),
                id="rating_minus_1",
                on_click=partial(on_quick_rating_change, item_id="-1"),
            ),
            Button(
                Const("-5"),
                id="rating_minus_5",
                on_click=partial(on_quick_rating_change, item_id="-5"),
            ),
            Button(
                Const("-10"),
                id="rating_minus_10",
                on_click=partial(on_quick_rating_change, item_id="-10"),
            ),
        ),
        Button(
            Const("✏️ Ввести точное значение"),
            id="exact_rating",
            on_click=on_change_rating_click,
        ),
    ),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, b, m: m.switch_to(CharacterManagementSG.character_menu),
    ),
    state=CharacterManagementSG.quick_rating,
    getter=get_character_data,
)


# Диалог для изменения уровня
async def on_level_input(
    message: Message, widget: ManagedTextInput, manager: DialogManager, text: str
):
    try:
        level = int(text)
        character_id = manager.dialog_data.get("character_id", 0)
        await api_client.update_character_level(character_id, level)
        await message.answer(f"✅ Уровень изменен на {level}")
        await manager.back()
    except ValueError:
        await message.answer("❌ Введите целое число")
    except Exception:
        await message.answer("❌ Ошибка при обновлении уровня")


level_window = Window(
    Const("Введите новый уровень персонажа:"),
    TextInput(
        id="level_input",
        on_success=on_level_input,
    ),
    Back(Const("⬅️ Назад")),
    state=CharacterManagementSG.change_level,
)

character_menu_window = Window(
    Multi(
        Format("🧙 Персонаж: {character.name}"),
        Format("⭐ Уровень: {character.level}"),
        Format("🏆 Рейтинг: {character.rating}"),
        sep="\n",
    ),
    Row(
        Button(Const("📈 Уровень"), id="change_level", on_click=on_change_level),
        Button(
            Const("🏆 Рейтинг"),
            id="change_rating",
            on_click=lambda c, b, m: m.switch_to(CharacterManagementSG.quick_rating),
        ),
    ),
    Row(
        Button(Const("🎒 Инвентарь"), id="view_inventory", on_click=on_view_inventory),
        Button(Const("📥 Скачать JPEG"), id="download_jpeg", on_click=on_download_jpeg),
    ),
    Back(Const("⬅️ Назад")),
    Cancel(Const("❌ Выход")),
    state=CharacterManagementSG.character_menu,
    getter=get_character_data,
)

# Собираем все диалоги
character_management_dialog = Dialog(
    company_window,
    character_window,
    character_menu_window,
    level_window,
    rating_window,
    quick_rating_window,
    *inventory_management_dialog.windows.values()
    # остальные окна...
)  # + inventory_management_dialog
