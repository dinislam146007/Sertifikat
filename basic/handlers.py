from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from search.search import find_certificates_for_product

router = Router()



@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Укажите тип вашей продукции во <b>множественном</b> числе, например:\n"
                        "<i>Шампунь >> шампуни</i>\n"
                        "<i>Микроволновки >> печи микроволновые</i>\n"
                        "<i>Зарядка >> устройства для зарядки</i>"
                        )


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
