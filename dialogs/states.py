from aiogram.fsm.state import State, StatesGroup

class CharacterManagementSG(StatesGroup):
    company_selection = State()
    character_selection = State()
    character_menu = State()
    change_level = State()
    change_rating = State()
    quick_rating = State()
    view_inventory = State()
    add_inventory_item = State()
    delete_inventory_item = State()