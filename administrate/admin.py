from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from amount.prices import get_amounts

router_admin = Router()

@router_admin.callback_query(F.data == 'admin')
async def admin_main(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_text(
        text='Админ', 
        reply_markup=admin_unine()
    )


@router_admin.callback_query(F.data.startswith('change_price'))
async def change_price(callback: CallbackQuery, ):
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
