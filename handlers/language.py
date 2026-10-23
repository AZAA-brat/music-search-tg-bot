from aiogram import F, Router
import asyncio
from utils.phrases import get_text
from utils.dictionaries import lang_memory
from keyboards.reply import rus, eng
router = Router()
LANG_CODE = {
    rus: "ru",
    eng: "en"
}
@router.message(F.text.in_([rus, eng]))
async def handle_language(message):
    lang_memory[message.from_user.id] = LANG_CODE[message.text]
    msg = await message.answer(get_text("lang_set", message.from_user.id))
    await asyncio.sleep(1)
    await msg.delete()