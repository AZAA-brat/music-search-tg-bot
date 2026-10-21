from aiogram import F, Router
import asyncio
import logging

from utils.phrases import get_text
from functions.search_engine import search_songs
from functions.slicer import firstslice
from functions.thumbnail import thumbnail
from utils.dictionaries import title_memory, link_memory, photo_msg_memory, search_memory
from keyboards.inline import quality_kb

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text, ~F.text.startswith("/"))
async def handle_any_text(message):
    if "youtube.com/" in message.text or "youtu.be" in message.text or "instagram.com" in message.text or "tiktok.com" in message.text:
        try:
            info = await asyncio.to_thread(thumbnail, message.text)
            title_memory[message.from_user.id] = info["title"]
            thumb_url = info["thumbnail"]
            link_memory[message.from_user.id] = message.text
            sent_photo = await message.answer_photo(thumb_url, caption=info["title"], reply_markup=quality_kb)
            photo_msg_memory[message.from_user.id] = sent_photo
        except Exception:
            logger.error("Thumbnail search failed", exc_info=True)
            await message.answer(get_text("error_photo_post", message.from_user.id))
            return
    else:
        try:
            results = await asyncio.to_thread(search_songs, message.text)
            result_url = results["entries"]
        except Exception:
            logger.error("Search results failed", exc_info=True)
            await message.answer(get_text("error_search", message.from_user.id))
            return
        if not result_url:
            await message.answer(get_text("error_search", message.from_user.id))
            return
        search_memory[message.from_user.id] = result_url
        text, keyboard = firstslice(result_url[0:10][11:20][21:30], message.from_user.id)
        header = get_text("search_results", message.from_user.id)
        text = header + "\n\n" + text
        await message.answer(text, reply_markup=keyboard)
