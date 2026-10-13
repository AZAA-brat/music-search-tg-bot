from aiogram import types
import asyncio
import os
from config import dp
from functions.extractor import simultaneous
from utils.phrases import get_text
from utils.dictionaries import search_memory
@dp.callback_query(lambda c: c.data.isdigit())
async def handle_user_choice(callback):
    index = int(callback.data) - 1
    chosen = search_memory[callback.from_user.id][index]
    link = chosen['webpage_url']
    status_msg = await callback.message.answer("⌛️")
    options = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "outtmpl": f"downloads/{callback.from_user.id}",
}
    try:
        info = await asyncio.to_thread(simultaneous, link, options)
    except Exception:
        await callback.message.answer(get_text("error_download", callback.from_user.id))
        return

    path = f"downloads/{callback.from_user.id}.mp3"
    filename = types.FSInputFile(f"downloads/{callback.from_user.id}.mp3", filename=f"{info['title']}.mp3")
    caption = f"{info['title']}, {info.get('uploader', 'Неизвестный')}"
    await callback.message.answer_audio(filename, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}")
    await status_msg.delete()
    os.remove(path)