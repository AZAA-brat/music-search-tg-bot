from aiogram import F
import asyncio
from functions.cleaner import clean_title
from functions.search_engine import search_songs
from functions.slicer import firstslice
from utils.phrases import get_text
from utils.dictionaries import search_memory, title_memory
from config import dp


@dp.callback_query(F.data == "download")
async def handle_inst_link(callback):
    title = title_memory[callback.from_user.id]
    title = clean_title(title)
    results = await asyncio.to_thread(search_songs, title)
    result_url = results["entries"]
    search_memory[callback.from_user.id] = result_url
    text, keyboard = firstslice(result_url[0:10])
    header = get_text("Search_results", callback.from_user.id)
    text = header + "\n\n" + text
    await callback.message.answer(text, reply_markup=keyboard)