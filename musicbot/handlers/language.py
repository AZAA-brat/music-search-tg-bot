from aiogram import F
from config import dp
from utils.phrases import lang_memory, get_text
@dp.callback_query(F.data.in_(["ru", "en"]))
async def handle_language(callback):
    lang_memory[callback.from_user.id] = callback.data
    await callback.message.answer(get_text("lang_set", callback.from_user.id))