import asyncio
import logging
from aiogram import Router
from aiogram.types import CallbackQuery

from functions.extractor import download_media
from functions.options import video_options
from handlers.sender import send_media
from keyboards.callbacks import QualityCB
from utils.dictionaries import link_memory
from utils.phrases import get_text

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(QualityCB.filter())
async def handle_quality(callback: CallbackQuery, callback_data: QualityCB):
    link = link_memory.get(callback.from_user.id, None)
    if link is None:
        await callback.message.answer(get_text("unknown", callback.from_user.id))
        return

    status_msg = await callback.message.answer("⌛️")
    options = video_options(callback.from_user.id, callback_data.quality)
    file_path = f"downloads/{callback.from_user.id}.mp4"

    try:
        info = await asyncio.to_thread(download_media, link, options)
    except Exception:
        logger.error("There was a problem downloading the media.", exc_info=True)
        await status_msg.delete()
        await callback.message.answer(get_text("error_download", callback.from_user.id))
        return

    await send_media(callback, file_path, True, info, status_msg)