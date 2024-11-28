from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from amount.prices import *
import asyncio
from messages.message import *
from db.db import *

router_admin = Router()

class Newsletter(StatesGroup):
    message = State()

class EditPrice(StatesGroup):
    new_price = State()

class EditMessage(StatesGroup):
    new_mes = State()


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

@router_admin.callback_query(F.data.startswith('edit_mes'))
async def edit_mes(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split()[1]
    if action == 'start':
        await callback.message.edit_text(
            text='Изменить:',
            reply_markup=edit_mes_inline()
        )
    else:
        msg = await callback.message.edit_text(
            text='Отправьте новое сообщение:',
            reply_markup=close_state_inline()
        ) 
        await state.set_state(EditMessage.new_mes)
        await state.update_data(
            last_msg=msg.message_id,
            action=action
        )


@router_admin.message(EditMessage.new_mes)
async def new_edit_mes(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
    if data['action'] == 'services':
        set_services(message.text)
    else:
        set_inf(message.text)
    msg = await message.answer('Сообщение обновлено')
    await asyncio.sleep(5)
    await msg.delete()

@router_admin.callback_query(F.data == 'newsletter')
async def newsletter(callback: CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text(
        text='Введите текст рассылки',
        reply_markup=close_state_inline()
    )
    await state.set_state(Newsletter.message)
    await state.update_data(last_msg=msg.message_id)

@router_admin.message(Newsletter.message)
async def newslet(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])

    users = get_all_user()
    msg = await message.answer(text=f'Ожидайте, рассылка будет проведена спустя {len(users) * 2}')
    for user in users:
        try:
            await bot.send_message(
                text=message.text
            )
            await asyncio.sleep(2)
        except Exception:
            pass
    await msg.delete()
    await message.answer('Рассылка проведена успешно!')


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