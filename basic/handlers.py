from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from search.search import find_certificates_for_product
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from amount.prices import get_amounts


router = Router()

def back_cert_type(cert: str):
    if cert == 'СГР':
        t = 3
        t1 = '0'
    elif cert.startswith('ТРТС'):
        t = 0
        t1 = cert.split()[1]
    else:
        t = 2
        t1 = '0'
    return [t, t1]

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
    text = 'Укажите тип вашей продукции во множественном числе, например:\n'
    text += '<i>Шампунь >> шампуни</i>\n'
    text += '<i>Микроволновки >> печи микроволновые</i>\n'
    text += '<i>Зарядка >> устройства для зарядки</i>'
    msg = await callback.message.edit_text(
        text=text,
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
            c = back_cert_type(cert)
            key.append([
                InlineKeyboardButton(text=cert, callback_data=f"cert {c[0]} {c[1]}")
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
        trts_type = callback.data.split()[2]
        if int(trts_type) == 0:
            text = 'Сертификат ТРТС'
            msg = 'Выберите тип сертификата:'
            trts_type = None
        else:
            text = f'ТРТС {trts_type}'
            msg = None
    elif cert_info == 1:
        trts_type = None
        text = 'Декларация ТРТС'
        msg = None
    elif cert_info == 2:
        trts_type = None
        text = 'ГОСТр'
        msg = None
    else:
        trts_type = None
        text = 'СГР'
        msg = None
    if not msg:
        data = get_amounts()
        msg = f"Сертификат: {text} \n Цена: {data[f'{text}']}"
    await callback.message.edit_text(
        text=msg,
        reply_markup=cert_inline(cert_info, trts_type)
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