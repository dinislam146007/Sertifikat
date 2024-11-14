from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_inline():
    kb = [
        [InlineKeyboardButton(text='Проверить продукцию', callback_data='search')],
        [InlineKeyboardButton(text='Сертификат ТРТС', callback_data='cert 0 0'),
        InlineKeyboardButton(text='Декларация ТРТС', callback_data='cert 1')],
        [InlineKeyboardButton(text='Сертификат ГОСТр', callback_data='cert 2'),
        InlineKeyboardButton(text='СГР', callback_data='cert 3')],
        [InlineKeyboardButton(text='Связь с менежером', url='https://t.me/Nastia_NZ')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)

def close_state_inline():
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data="close_state")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def cert_inline(type_cert, trts_type):
    kb = [
    ]
    if (type_cert == 0) and (trts_type is not None):
        kb.append([InlineKeyboardButton(text='ТРТС 004', callback_data='cert 0 004')])
        kb.append([InlineKeyboardButton(text='ТРТС 010', callback_data='cert 0 010')])
        kb.append([InlineKeyboardButton(text='ТРТС 018', callback_data='cert 0 018')])
        kb.append([InlineKeyboardButton(text='ТРТС 020', callback_data='cert 0 020')])
    else:

        kb.append(
            [InlineKeyboardButton(text='Оставить заявку', callback_data=f'request {type_cert} {trts_type}')], 
        )
    kb.append(
        [InlineKeyboardButton(text='Назад', callback_data="close_state")]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb)

def trts_inline():
    kb = [
        [InlineKeyboardButton(text='ТРТС 004', callback_data='cert trts')],
        [InlineKeyboardButton(text='ТРТС 010', callback_data='cert trts')],
        [InlineKeyboardButton(text='ТРТС 018', callback_data='cert trts')],
        [InlineKeyboardButton(text='ТРТС 020', callback_data='cert trts')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)