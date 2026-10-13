from aiogram import types
import asyncio
import os
from config import dp
from functions.extractor import simultaneous
from utils.phrases import get_text
from utils.dictionaries import photo_msg_memory, memory

@dp.callback_query()
async def handle_buttons(callback):
    status_msg = await callback.message.answer("⌛️")
    link = memory[callback.from_user.id]
    if callback.data == "audio":
        options = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
    }],
    "outtmpl": f"downloads/{callback.from_user.id}",
}
        filename = types.FSInputFile(f"downloads/{callback.from_user.id}.mp3")
    else:
        options = {"format": f"bestvideo[height<={callback.data}]+bestaudio/best",
                   "outtmpl": f"downloads/{callback.from_user.id}.%(ext)s"}
    try:
        info = await asyncio.to_thread(simultaneous, link, options)
    except Exception:
        await callback.message.answer(get_text("error_download", callback.from_user.id))
        return
    if callback.data == "audio":
        path = f"downloads/{callback.from_user.id}.mp3"
        filename = types.FSInputFile(f"downloads/{callback.from_user.id}.mp3", filename=f"{info['title']}.mp3")
        caption = f"{info['title']}, {info.get('uploader', 'Неизвестный')}"
        await callback.message.answer_audio(filename, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}")
        await status_msg.delete()
        photo_msg = photo_msg_memory.get(callback.from_user.id)
        if photo_msg:
            await photo_msg.delete()
        os.remove(path)
    else:
        path2 = f"downloads/{callback.from_user.id}.mp4"
        filename2 = types.FSInputFile(f"downloads/{callback.from_user.id}.mp4")
        caption = f"{info['title']}, {info.get('uploader', 'Неизвестный')}"
        await callback.message.answer_video(filename2, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}")
        await status_msg.delete()
        photo_msg = photo_msg_memory.get(callback.from_user.id)
        if photo_msg:
            await photo_msg.delete()
        os.remove(path2)
