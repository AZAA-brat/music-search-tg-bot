from aiogram import F, types, Router
from utils.phrases import get_text
from functions.search_engine import search_songs
from functions.slicer import firstslice
from functions.thumbnail import thumbnail
import asyncio
import logging
from utils.dictionaries import title_memory, memory, photo_msg_memory, search_memory
from keyboards.inline import quality_kb
logger = logging.getLogger(__name__)
router = Router()
@router.message(F.text)
async def handle_any_text(message):
    if "http" in message.text:
        try:
            info = await asyncio.to_thread(thumbnail, message.text)
        except Exception:
            logger.error("Thumbnail search failed")
            await message.answer(get_text("error_photo_post", message.from_user.id))
            return
        title_memory[message.from_user.id] = info["title"]
        thumb_url = info["thumbnail"]
        memory[message.from_user.id] = message.text
        if "instagram.com" in message.text:
            quality_kb.append([types.InlineKeyboardButton(text="📥 download audio", callback_data="download")])
        kb = types.InlineKeyboardMarkup(inline_keyboard=quality_kb)

        sent_photo = await message.answer_photo(thumb_url, caption=info["title"], reply_markup=kb)
        photo_msg_memory[message.from_user.id] = sent_photo
    else:
        try:
            results = await asyncio.to_thread(search_songs, message.text)
        except Exception:
            await message.answer(get_text("error_search", message.from_user.id))
            return
        result_url = results["entries"]
        if not result_url:
            await message.answer(get_text("error_search", message.from_user.id))
            return
        search_memory[message.from_user.id] = result_url
        text, keyboard = firstslice(result_url[0:10])
        header = get_text("search_results", message.from_user.id)
        text = header + "\n\n" + text
        await message.answer(text, reply_markup=keyboard)