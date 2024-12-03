from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_inline(admin=False):
    kb =[
        [InlineKeyboardButton(text='🔎 Проверить стоимость по названию', callback_data='search')],
        [InlineKeyboardButton(text='📑 Все наши услуги', callback_data='services')],
        [InlineKeyboardButton(text='⁉️ Проконсультироваться с экспертом', url='https://t.me/Nastia_NZ')],
        [InlineKeyboardButton(text='⚠️ Важная и полезная информация', callback_data='inf')],
        [InlineKeyboardButton(text='📞 Наши контакты', url='https://t.me/Nastia_NZ')]
    ]
    if admin:
        kb.append(
            [InlineKeyboardButton(text='Администратору', callback_data='admin')]
        )
    return InlineKeyboardMarkup(inline_keyboard=kb)

def services_inline():
    kb = [
        [InlineKeyboardButton(text='🔎 Проверить стоимость по названию', callback_data='search')],
        [InlineKeyboardButton(text='Сертификат ТРТС', callback_data='cert 0 0'),
        InlineKeyboardButton(text='Декларация ТРТС', callback_data='cert 1')],
        [InlineKeyboardButton(text='Сертификат ГОСТр', callback_data='cert 2'),
        InlineKeyboardButton(text='СГР', callback_data='cert 3')],
        [InlineKeyboardButton(text='Связь с менежером', url='https://t.me/Nastia_NZ')],
        [InlineKeyboardButton(text='Назад', callback_data='close_state')]
    ]
    # if admin:
    #     kb.append(
    #         [InlineKeyboardButton(text='Администратору', callback_data='admin')]
    #     )
    return InlineKeyboardMarkup(inline_keyboard=kb)

def close_state_inline():
    kb = [
        [InlineKeyboardButton(text='Назад', callback_data="close_state")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def cert_inline(type_cert, trts_type):
    kb = [
    ]
    if (type_cert == 0) and (trts_type is None):
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

def admin_unine():
    kb = [
        [InlineKeyboardButton(text='Изменить цены на сертификацию', callback_data='change_price start')],
        [InlineKeyboardButton(text='Изменить сообщение', callback_data='edit_mes start')],
        [InlineKeyboardButton(text='Запустить рассылку', callback_data='newsletter')],
        [InlineKeyboardButton(text='Заявки', callback_data='sh_requests 0')],
        [InlineKeyboardButton(text='Назад', callback_data='close_state')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def edit_mes_inline():
    kb = [
        [InlineKeyboardButton(text='Стартовое сообщение', callback_data='edit_mes start_m')],
        [InlineKeyboardButton(text='Сообщение услуг', callback_data='edit_mes services')],
        [InlineKeyboardButton(text='Сообщение информации', callback_data='edit_mes inf')],
        [InlineKeyboardButton(text='Сообщение поиска', callback_data='edit_mes search')],
        [InlineKeyboardButton(text='Назад', callback_data='admin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def change_price_inline():
    kb = [
        [InlineKeyboardButton(text='ТРТС 004', callback_data='change_price 0 004'),
         InlineKeyboardButton(text='ТРТС 010', callback_data='change_price 0 010'),
         InlineKeyboardButton(text='ТРТС 018', callback_data='change_price 0 018'),
         InlineKeyboardButton(text='ТРТС 020', callback_data='change_price 0 020')
         ],
         [InlineKeyboardButton(text='Декларация ТРТС', callback_data='change_price 1')],
         [InlineKeyboardButton(text='ГОСТр', callback_data='change_price 2')],
         [InlineKeyboardButton(text='СГР', callback_data='change_price 3')],
        [InlineKeyboardButton(text='Назад', callback_data='admin')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def request_choice():
    kb = [
        [
            InlineKeyboardButton(text='Скачать бланк', callback_data='choice_request blank'),
         InlineKeyboardButton(text='Заполнить сейчас', callback_data='choice_request now')
         ],
         [InlineKeyboardButton(text='Отмена', callback_data='close_state')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def search_answer_inline():
    kb = [
        [InlineKeyboardButton(text='Уточнить у менеджера', url='https://t.me/Nastia_NZ')],
        [InlineKeyboardButton(text='Попробовать ввести ещё раз', callback_data='search')],
        [InlineKeyboardButton(text='Назад', callback_data='close_state')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def requests_inline(n):
    kb = [
        [InlineKeyboardButton(text='<-', callback_data=f'requests {n - 1}'),
         InlineKeyboardButton(text='Назад', callback_data='admin'),
         InlineKeyboardButton(text='->', callback_data=f'requests {n + 1}')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)