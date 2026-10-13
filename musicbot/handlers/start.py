from aiogram import types
from aiogram.filters import Command
from utils.phrases import get_text
from config import dp

@dp.message(Command("start"))
async def handle_message(message):
    keb = types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(
               text = "Русский 🇷🇺", callback_data = "ru"),
            types.InlineKeyboardButton(
               text = "English 🇬🇧", callback_data = "en")
]])
    await message.answer(get_text("greeting", message.from_user.id), reply_markup = keb)