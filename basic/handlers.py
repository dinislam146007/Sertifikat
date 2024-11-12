from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from search.search import find_certificates_for_product

router = Router()


@router.message(Command("start"))
async def send_welcome(message: Message):
    kb = [
        [InlineKeyboardButton(text='Проверить продукцию', callback_data='search')],
        [InlineKeyboardButton(text='Сертификат ТРТС', callback_data='cert СТРТС'),
        InlineKeyboardButton(text='Декларация ТРТС', callback_data='cert ДТРТС')],
        [InlineKeyboardButton(text='Сертификат ГОСТр', callback_data='cert ГОСТр'),
        InlineKeyboardButton(text='СГР', callback_data='cert СГР')],
        [InlineKeyboardButton(text='Связь с менежером', url='https://t.me/Nastia_NZ')]
    ]
    await message.answer("Привет. Это бот сертификации. Напиши что хочешь"
    ,reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
                        )


@router.callback_query(F.data.stertswith('cert'))
async def cert(callback: CallbackQuery):
    cert_info = callback.data.split()[1]
    await callback.message.edit_text(f'{cert_info}')



@router.message()
async def send_certificate(message: Message):
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
        msg = "Тип сертификата для этого товара не найден."
        await message.answer(msg)

