from aiogram import types, Router
from aiogram.types import CallbackQuery, Audio
import asyncio
import os
import logging
from functions.extractor import download_media
from functions.options import audio_options, video_options
from utils.phrases import get_text
from utils.dictionaries import photo_msg_memory, memory, link_memory
from handlers.sender import send_media
from keyboards.callbacks import QualityCB, AudioCB
router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(QualityCB.filter())
async def handle_quality(callback: CallbackQuery, callback_data: QualityCB):
    status_msg = await callback.message.answer("⌛️")
    link = link_memory.get(callback.from_user.id, None)
    if link is None:
        await callback.message.answer(get_text("unknown", callback.from_user.id))
        return
    options = video_options(user_id, callback_data.quality)
    try:
        info = await asyncio.to_thread(download_media, link, options)
    except Exception:
        logger.error("There was a problem downloading the media.", exc_info=True)
        await callback.message.answer(get_text("error_download", callback.from_user.id))
        return


@router.callback_query(AudioCB.filter())
async def handle_audio(callback: CallbackQuery, callback_data: audio):


