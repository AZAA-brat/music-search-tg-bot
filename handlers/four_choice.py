from aiogram import Router
from aiogram.filters import Command
from utils.phrases import get_text
from keyboards.inline import choice_kb
router = Router()

@router.message(Command("choice"))
async def choice(message):
    await message.answer(get_text("choice", message.from_user.id), reply_markup=choice_kb)