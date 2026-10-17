from aiogram.types import CallbackQuery
from aiogram import types
import os
import logging
from utils.dictionaries import photo_msg_memory
from utils.phrases import get_text
logger = logging.getLogger(__name__)
async def send_media(callback: CallbackQuery, file_path: str, is_video: bool, info, status_msg):
    try:
        media_file = types.FSInputFile(file_path)
        caption = f"{info['title']}, {info.get('uploader', get_text('unknown', callback.from_user.id))}"
        if is_video:
            await callback.message.answer_video(media_file, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}")
        else:
            title = info['title']
            performer = info.get('artist') or info.get('uploader', get_text('unknown', callback.from_user.id))
            await callback.message.answer_audio(media_file, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}", title=title, performer=performer)
    except Exception:
        logger.exception("Couldn't send media file")
        await callback.message.answer(get_text("error_download", callback.from_user.id))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        await status_msg.delete()
        photo_msg = photo_msg_memory.get(callback.from_user.id)
        if photo_msg:
            await photo_msg.delete()
