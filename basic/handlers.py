from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from search.search import find_certificates_for_product
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup


router = Router()

class SearchState(StatesGroup):
    text = State()

    
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        text="Привет",
        reply_markup=start_inline()  
    )
                        
@router.callback_query(F.data == 'close_state')
async def close_state(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await callback.answer("Ожидание ответа успешно отменено.")
    await callback.message.edit_text(
        text="Привет",
        reply_markup=start_inline()  
    )

@router.callback_query(F.data == 'search')
async def search(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(
        text='Введите названи е вашей продукции',
        reply_markup=close_state()
    )
    await state.set_state(SearchState.text)

@router.message(SearchState.text)
async def search_state(message: Message, state: FSMContext):
    product_name = message.text.strip().lower()
    certificates = find_certificates_for_product(product_name)

    if certificates:
        unique_certificates = []
        msg = f"Найденные совпадения для товара <b>{product_name}</b>:\n"

        for item, cert_type in certificates:
            if cert_type not in unique_certificates:
                unique_certificates.append(cert_type)
            msg += f"- {item} <b>(Тип сертификата: {cert_type})</b>\n"
        key = []
        for cert in unique_certificates:
            key.append([
                InlineKeyboardButton(text=cert, callback_data=f'cert {cert}')
            ])
        keyboard = InlineKeyboardMarkup(inline_keyboard=key)

        await message.answer(msg, reply_markup=keyboard)
    else:
        msg = "Тип сертификата для этого товара не найден."
        await message.answer(msg)


@router.callback_query(F.data.startswith('cert'))
async def cert(callback: CallbackQuery):
    cert_info = int(callback.data.split()[1])
    if cert_info == 0:
        text = 'Сертификат ТРТС'
    elif cert_info == 1:
        text = 'Декларация ТРТС'
    elif cert_info == 2:
        text = 'Сертификат ГОСТр'
    else:
        text = 'СГР'
    await callback.message.edit_text(text=f'Сертификат: {text}')
