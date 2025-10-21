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
    add_inventory_item_description = State()
    add_inventory_item_quantity = State()
    delete_inventory_item = State()
    edit_inventory_item = State()
    edit_inventory_item_name = State()
    edit_inventory_item_description = State()
    edit_inventory_item_quantity = State()
