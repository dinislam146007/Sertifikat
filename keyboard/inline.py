from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_inline():
    kb = [
        [InlineKeyboardButton(text='Проверить продукцию', callback_data='search')],
        [InlineKeyboardButton(text='Сертификат ТРТС', callback_data='cert 0'),
        InlineKeyboardButton(text='Декларация ТРТС', callback_data='cert 1')],
        [InlineKeyboardButton(text='Сертификат ГОСТр', callback_data='cert 2'),
        InlineKeyboardButton(text='СГР', callback_data='cert 3')],
        [InlineKeyboardButton(text='Связь с менежером', url='https://t.me/Nastia_NZ')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def close_state():
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data="close_state")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


