from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

rating_display_router = Router()


class RatingStates(StatesGroup):
    main = State()


rating_display_dialog = Dialog(
    Window(
        Format("Ну тут рейтинг будет короче")
    )
)