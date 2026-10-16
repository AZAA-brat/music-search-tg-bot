from aiogram import F, Router
import asyncio

from unicodedata import lookup

from functions.cleaner import clean_title
from functions.search_engine import search_songs
from functions.slicer import firstslice
from utils.phrases import get_text
from utils.dictionaries import search_memory, title_memory
router = Router()
@router.callback_query(F.data == "download")
async def handle_inst_audio(callback):
    title = title_memory.get(callback.from_user.id, None)
    if title is None:
        await callback.message.answer(get_text("resend", callback.from_user.id))
        return
    title = clean_title(title)
    results = await asyncio.to_thread(search_songs, title)
    result_url = results["entries"]
    if not result_url:
        await callback.message.answer(get_text("error_search", callback.from_user.id))
        return
    search_memory[callback.from_user.id] = result_url
    text, keyboard = firstslice(result_url[0:10])
    header = get_text("search_results", callback.from_user.id)
    text = header + "\n\n" + text
    await callback.message.answer(text, reply_markup=keyboard)