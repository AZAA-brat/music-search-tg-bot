from aiogram import types, Router
import asyncio
import os
import logging
from aiogram.types import CallbackQuery

from functions.extractor import download_media
from utils.phrases import get_text
from utils.dictionaries import search_memory
from keyboards.callbacks import PickCB
from functions.options import audio_options
from handlers.sender import send_media

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(PickCB.filter())
async def handle_user_choice(callback: CallbackQuery, callback_data: PickCB):
    try:
        index = callback_data.index - 1
        chosen = search_memory[callback.from_user.id][index]
        link = chosen['webpage_url']
        options = audio_options(callback.from_user.id)
        info = await asyncio.to_thread(download_media, link, options)
    except Exception:
        logger.error("Error downloading media", exc_info=True)
        await callback.message.answer(get_text("error_download", callback.from_user.id))
        return
    status_msg = await callback.message.answer("⌛️")
    file_path = f"downloads/{callback.from_user.id}.mp3"
    await send_media(callback, file_path, False, info, status_msg)