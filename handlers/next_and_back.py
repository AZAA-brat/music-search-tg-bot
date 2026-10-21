from aiogram import Router
from aiogram.types import CallbackQuery

from utils.phrases import get_text
from keyboards.callbacks import PageCB
from functions.slicer import firstslice
from utils.dictionaries import search_memory
router = Router()

@router.callback_query(PageCB.filter())
async def handle_page(callback: CallbackQuery, callback_data: PageCB):
    await callback.answer()
    entries = search_memory.get(callback.from_user.id)
    if not entries:
        await callback.message.answer(get_text("resend", callback.from_user.id))
        return
    text, keyboard = firstslice(entries, callback.from_user.id, callback_data.page)
    header = get_text("search_results", callback.from_user.id)
    await callback.message.edit_text(header + "\n\n" + text, reply_markup=keyboard)