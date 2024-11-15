from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from amount.prices import *

router_admin = Router()


class EditPrice(StatesGroup):
    new_price = State()

def type_cert(t, t1):
    if t == '0':
        return f'ТРТС {t1}'
    elif t == '1':
        return 'Декларация ТРТС'
    elif t == '2':
        return 'ГОСТр'
    else:
        return 'СГР'

@router_admin.callback_query(F.data == 'admin')
async def admin_main(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(
        text='Админ', 
        reply_markup=admin_unine()
    )


@router_admin.callback_query(F.data.startswith('change_price'))
async def change_price(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split()[1]
    if action == 'start':
        data = get_amounts()
        text = 'Цены услуг на данный момент\n'
        text += f"ТРТС 004: {data['ТРТС 004']}\n"
        text += f"ТРТС 010: {data['ТРТС 010']}\n"
        text += f"ТРТС 018: {data['ТРТС 018']}\n"
        text += f"ТРТС 020: {data['ТРТС 020']}\n"
        text += f"Декларация ТРТС: {data['Декларация ТРТС']}\n"
        text += f"ГОСТр: {data['ГОСТр']}\n"
        text += f"СГР: {data['СГР']}"
        await callback.message.edit_text(
            text=text,
            reply_markup=change_price_inline()
        )
    else:
        if action == '0':
            t1 = callback.data.split()[2]
        else:
            t1 = None
        msg = await callback.message.edit_text(
            text='Введите числовое значение',
            reply_markup=close_state_inline()
        )
        await state.set_state(EditPrice.new_price)
        await state.update_data(cert=type_cert(action, t1), last_msg=msg.message_id)


@router_admin.message(EditPrice.new_price)
async def new_price(message: Message, state: FSMContext, bot: Bot):
    try:
        data_state = await state.get_data()
        new_price = int(message.text)
        await bot.delete_message(message_id=data_state['last_msg'], chat_id=message.from_user.id)
        data = get_amounts()
        data[data_state['cert']] = new_price
        set_amounts(data)
        await message.answer('Значение изменено!')
    except ValueError:
        await message.answer('Введите число!', reply_markup=close_state_inline())