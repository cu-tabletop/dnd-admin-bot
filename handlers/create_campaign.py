import requests
from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

campaign_create_router = Router()

class CreateCampaignStates(StatesGroup):
    waiting_for_name = State()


# TODO: Сейчас Телеграм возвращает ошибку, не уверен, в чём дело:
# * Error: Telegram server says - Bad Request: can't parse entities: 
# * Unsupported start tag "!doctype" at byte offset 55

@campaign_create_router.message(Command("create_campaign"))
async def start_campaign_creation(message: types.Message, state: FSMContext):

    await message.answer(text="Введите название кампании: ")
        
    await state.set_state(CreateCampaignStates.waiting_for_name)


@campaign_create_router.message(CreateCampaignStates.waiting_for_name)
async def process_campaign_name(message: types.Message, state: FSMContext):
    
    campaign_data = message.text.strip()
    
    campaign_data = {
        'telegram_id': 0,
        'title': 0,
        'description': 0,
        'icon': 0,
    }
    
    try:

        response = requests.post(
            'http://localhost:8000/api/campaign/create',
            json=campaign_data,
        )
        
        if response.status_code == 201: 
            await message.answer(f"Кампания {campaign_data['title']} создана")

        else:
            error_msg = response.text
            await message.answer(f"Ошибка при создании кампании ({error_msg})")
            
    except Exception as e:
        await message.answer(f"Internal Error: {str(e)}")
    
    await state.clear()


@campaign_create_router.message(Command("cancel"))
@campaign_create_router.message(F.text.casefold() == "cancel")
async def cancel_creation(message: types.Message, state: FSMContext):

    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Уже отменена?..")
        return
    
    await state.clear()

    await message.answer("Создание отменено")