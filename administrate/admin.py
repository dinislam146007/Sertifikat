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
        text='Админ'
    )
