from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel, Back, Column
from aiogram_dialog.widgets.text import Const, Format

from .campaign_interaction import CampaignInteractionStates

characters_display_router = Router()

CHARACTERS = [
# ! Предполагается что мы будем фетчить это из ДБ
# ! Данный функционал ещё не реализован
    {"id": 1, "name": "Baba"},
    {"id": 2, "name": "Is You"}
]


class CharsInteractionStates(StatesGroup):
    main = State()


async def on_character_selected(message: Message, button: Button, 
                                dialog_manager: DialogManager):
     
    pass


async def on_cancel(message: CallbackQuery, button: Button,
                    dialog_manager: DialogManager):
     
    pass


def create_character_buttons(characters):
        
        buttons = []
        for character in characters:
            button_text = f"{character['name']}"
            buttons.append(
                Button(
                    Const(button_text),
                    id=f"character_{character['id']}",
                    on_click=on_character_selected,
                )
            )
        return Column(*buttons)


characters_display_dialog = Dialog(
    Window(
        Format("**Панель взаимодействия с персонажами"),
        create_character_buttons(CHARACTERS),
        Cancel(Const("Назад")),
        state=CharsInteractionStates.main
    ),
)
