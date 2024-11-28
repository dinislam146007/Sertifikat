from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from search.search import find_certificates_for_product
from keyboard.inline import *
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from amount.prices import get_amounts
from administrate.admin_file import *
from aiogram.types import InputFile, FSInputFile
from documents.document import doc
from messages.message import *
from db.db import *

router = Router()

def type_cert(t, t1):
    if t == '0':
        return f'ТРТС {t1}'
    elif t == '1':
        return 'Декларация ТРТС'
    elif t == '2':
        return 'ГОСТр'
    else:
        return 'СГР'

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
    choice = State()
    one = State()
    two = State()
    three = State()
    four = State()
    phone = State()
    address = State()
    name = State()
    
@router.message(Command("start"))
async def send_welcome(message: Message):
    if message.from_user.id in get_admins():
        admin = True
    else:
        admin = False
    if not get_user(message.from_user.id):
        set_user(message.from_user.id, message.from_user.username)

    await message.answer(
        text="Привет",
        reply_markup=start_inline(admin=admin)  
    )
                        
@router.callback_query(F.data == 'close_state')
async def close_state(callback: CallbackQuery, state: FSMContext):
    try:
        current_state = await state.get_state()
        await state.clear()
    except Exception:
        pass
    if callback.from_user.id in get_admins():
        admin = True
    else:
        admin = False

    await callback.message.edit_text(
        text="Привет",
        reply_markup=start_inline(admin)  
    )


@router.callback_query(F.data == 'search')
async def search(callback: CallbackQuery, state: FSMContext):
    # text = 'Укажите тип вашей продукции во множественном числе, например:\n'
    # text += '<i>Шампунь >> шампуни</i>\n'
    # text += '<i>Микроволновки >> печи микроволновые</i>\n'
    # text += '<i>Зарядка >> устройства для зарядки</i>'
    msg = await callback.message.edit_text(
        text=get_search(),
        reply_markup=search_answer_inline()
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
        await message.answer(
            text=msg,
            reply_markup=search_answer_inline())
    await state.clear()


@router.callback_query(F.data.startswith('cert'))
async def cert(callback: CallbackQuery):
    cert_info = int(callback.data.split()[1])
    data = get_amounts()
    # await callback.message.answer(f"{callback.data}")
    # msg = f"Произошла ошибка, сертификат не найден. {callback.data}"  # Значение по умолчанию
    if cert_info == 0:
        trts_type = callback.data.split()[2]
        if int(trts_type) == 0:
            text = 'Сертификат ТРТС'
            msg = 'Выберите нужный регламент:'
            trts_type = None
        else:
            text = f'ТРТС {trts_type}'
            msg = f"Сертификат: {text} \nЦена: {data[f'{text}']}"
    elif cert_info == 1:
        trts_type = None
        text = "Декларация ТРТС"
        msg = f"{text}\n"
        msg += f"Цена: {data[f'{text}']}\n"
        msg += "Оформление 2 дня\n"
        msg += "Срок действия 5 лет"
        # msg = None
    
    elif cert_info == 2:
        trts_type = None
        text = 'ГОСТр'
        msg = f"Сертификат {text}\n"
        msg += f"Цена: {data[f'{text}']}\n"
        msg += "Оформление 2 дня\n"
        msg += f"Срок действия 3 года\n"
        msg += f"Протокол испытаний в подарок"
        # msg = None
    else:
        trts_type = None
        text = 'СГР'
        msg = f"Свидетельство Государственной Регистрации\n"
        msg += f"Цена: {data[f'{text}']}\n"
        msg += "Оформление до 10 недель\n"
        msg += "Выдаётся Бессрочно"
        # msg = None
    # if msg is None:
    #     msg = f"Сертификат: {text} \nЦена: {data[f'{text}']}"
    await callback.message.edit_text(
        text=msg,
        reply_markup=cert_inline(cert_info, trts_type)
        )

@router.callback_query(F.data.startswith('request'))
async def request(callback: CallbackQuery, state: FSMContext):
    info = callback.data.split()[1]
    if info == '0':
        t1 = callback.data.split()[2]
    else:
        t1 = None

    msg = await callback.message.edit_text(
        text='Выберите',
        reply_markup=request_choice()
    )
    await state.set_state(RequestForm.choice)
    await state.update_data(msg=msg.message_id, type_cert=type_cert(info, t1))

@router.callback_query(F.data == 'services')
async def services(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'{get_services()}',
        reply_markup=services_inline()
    )


@router.callback_query(F.data == 'inf')
async def services(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f'{get_inf()}',
        reply_markup=close_state_inline()
    )



@router.callback_query(F.data.startswith('choice_request'), RequestForm.choice)
async def choice_request(callback: CallbackQuery, state: FSMContext, bot: Bot):
    action = callback.data.split()[1]
    data = await state.get_data()
    if action == 'blank':
        await callback.message.answer_document(
            FSInputFile(path=doc)
        )
        await bot.delete_message(message_id=data['msg'], chat_id=callback.from_user.id)
    else:
        text = "Введите название организации:"
        msg = await callback.message.edit_text(text, reply_markup=close_state_inline())
        await state.set_state(RequestForm.name)
        await state.update_data(last_msg=msg.message_id)


@router.message(RequestForm.name)
async def request_name(message: Message, state: FSMContext, bot: Bot):
    # Сохранение названия организации
    await state.update_data(name=message.text)
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])

    # Запрос следующего поля
    text = "Введите место нахождения и адрес места осуществления деятельности:"
    msg = await message.answer(text, reply_markup=close_state_inline())
    await state.set_state(RequestForm.address)
    await state.update_data(last_msg=msg.message_id)


@router.message(RequestForm.address)
async def request_address(message: Message, state: FSMContext, bot: Bot):
    # Сохранение адреса
    await state.update_data(street=message.text)
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])

    # Запрос следующего поля
    text = "Введите телефон:"
    msg = await message.answer(text, reply_markup=close_state_inline())
    await state.set_state(RequestForm.one)
    await state.update_data(last_msg=msg.message_id)


    

@router.message(RequestForm.one)
async def request_one(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.update_data(
        phone=message.text,
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
    text = 'Принято! Теперь также через запятую введи: \n\n'
    text += '-email\n'
    text += '-ИНН\n'
    text += '-КПП\n'
    text += '-ОГРН\n'
    text += '-Руководитель (должность ФИО)\n'
    text += '-Дополнительно\n'
    msg = await message.answer(text, reply_markup=close_state_inline())
    await state.set_state(RequestForm.two)
    await state.update_data(last_msg=msg.message_id)


@router.message(RequestForm.two)
async def request_two(message: Message, state: FSMContext, bot: Bot):
    data_text = message.text.split(',')
    data = await state.get_data()
    await state.update_data(
        email=data_text[0],
        inn=data_text[1],
        kpp=data_text[2],
        ogrn=data_text[3],
        boss=data_text[4],
        more=data_text[5]
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
    text = 'Принято! Теперь также через запятую введи: \n\n'
    text += '-Наименование продукции\n'
    text += '-Протокол испытаний ЭЗ\n'
    text += '-Торговая марка\n'
    text += '-ОКПД2\n'
    text += '-ТНВЭД\n'
    text += '-Контркат\n'
    text += '-ДУЛ\n'
    text += '-Количество\n'
    msg = await message.answer(text, reply_markup=close_state_inline())
    await state.set_state(RequestForm.three)
    await state.update_data(last_msg=msg.message_id)

@router.message(RequestForm.three)
async def request_three(message: Message, state: FSMContext, bot: Bot):
    data_text = message.text.split(',')
    data = await state.get_data()
    await state.update_data(
        name_prod=data_text[0],
        trial=data_text[1],
        mark=data_text[2],
        okpd2=data_text[3],
        tnv=data_text[4],
        kontrkt=data_text[5],
        dyl=data_text[6],
        counnt=data_text[7],
    )
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
    text = 'Принято! Теперь также через запятую введи: \n\n'
    text += '-Название организации\n'
    text += '-Адрес места нахождения\n'
    text += '-Дополнительно\n'
    msg = await message.answer(text, reply_markup=close_state_inline())
    await state.set_state(RequestForm.four)
    await state.update_data(last_msg=msg.message_id)


@router.message(RequestForm.four)
async def request_three(message: Message, state: FSMContext, bot: Bot):
    data_text = message.text.split(',')
    await state.update_data(
        name_org=data_text[0],
        street_org=data_text[1],
        more_add=data_text[2],
    )
    data = await state.get_data()
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
    t = data['type_cert']
    msg = f'Заявка на {t} от @{message.from_user.username}\n\n'
    msg += f"1. Название организации: {data['name']}\n"
    msg += f"2. Место нахождения и адрес места осуществления деятельности: {data['street']}\n"
    msg += f"3. Телефон: {data['phone']}\n"
    msg += f"5. Email: {data['email']}\n"
    msg += f"6. ИНН: {data['inn']}\n"
    msg += f"7. КПП: {data['kpp']}\n"
    msg += f"8. ОГРН: {data['ogrn']}\n"
    msg += f"9. Руководитель (должность ФИО): {data['boss']}\n"
    msg += f"10. Дополнительно: {data['more']}\n"
    msg += f"11. Наименование продукции: {data['name_prod']}\n"
    msg += f"12. Протокол испытаний ЭЗ: {data['trial']}\n"
    msg += f"13. Торговая марка: {data['mark']}\n"
    msg += f"14. ОКПД2: {data['okpd2']}\n"
    msg += f"15. ТНВЭД: {data['tnv']}\n"
    msg += f"16. Контракт: {data['kontrkt']}\n"
    msg += f"17. ДУЛ: {data['dyl']}\n"
    msg += f"18. Количество: {data['counnt']}\n"
    msg += f"19. Название организации: {data['name_org']}\n"
    msg += f"20. Адрес места нахождения: {data['street_org']}\n"
    msg += f"21. Дополнительно: {data['more_add']}\n"
    await  bot.send_message(
        text=msg,
        chat_id=6634277726
    )
    text = 'Заявка отправлена! '
    msg = await message.answer(text)

    await state.clear()


    



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