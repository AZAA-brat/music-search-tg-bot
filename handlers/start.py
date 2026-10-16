from aiogram import Router
from aiogram.filters import Command
from utils.phrases import get_text
from keyboards.reply import lang_kb
router = Router()

@router.message(Command("start"))
async def handle_start(message):
    await message.answer(get_text("greeting", message.from_user.id), reply_markup = lang_kb)