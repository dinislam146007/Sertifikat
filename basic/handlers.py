from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from search.search import find_certificates_for_product
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup


router = Router()

class SearchState(StatesGroup):
    text = State()

class RequestForm(StatesGroup):
    phone = State()
    
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        text="Привет",
        reply_markup=start_inline()  
    )
                        
@router.callback_query(F.data == 'close_state')
async def close_state(callback: CallbackQuery, state: FSMContext):
    try:
        current_state = await state.get_state()
        await state.clear()
    except Exception:
        pass
    await callback.message.edit_text(
        text="Привет",
        reply_markup=start_inline()  
    )

@router.callback_query(F.data == 'search')
async def search(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(
        text='Введите названи е вашей продукции',
        reply_markup=close_state_inline()
    )
    await state.set_state(SearchState.text)
    await state.update_data(msg=msg.message_id)


@router.message(SearchState.text)
async def search_state(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(message_id=data['msg'], chat_id=message.from_user.id)
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
        msg = "Тип сертификата для этого товара не найден"
        await message.answer(\
            text=msg,
            reply_markup=close_state_inline())
    await state.clear()


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
    await callback.message.edit_text(
        text=f'Сертификат: {text} \n Цена: цена',
        reply_markup=cert_inline(cert_info)
        )

@router.callback_query(F.data.startswith('request'))
async def request(callback: CallbackQuery, state: FSMContext):
    info = callback.data.split()[1]
    msg = await callback.message.edit_text(
        text='Введите номер телефона',
        reply_markup=close_state_inline()
    )
    await state.set_state(RequestForm.phone)
    await state.update_data(msg=msg.message_id)


@router.message(RequestForm.phone)
async def request_phone(message: Message, state: FSMContext, bot: Bot):
    phone = message.text
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg'])
    await state.update_data(phone=phone)
    await message.answer(
        text='Заявка отправлена',
        reply_markup=close_state_inline()
    )
    await bot.send_message(chat_id=2047427176, 
                           text='Вам пришла заявка!\n'
                           f'Телефон: {phone}'
                           f'Username: @{message.from_user.username}'
                           f'ID: {message.from_user.id}'
                           )
    await state.clear()