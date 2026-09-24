from aiogram import F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
import asyncio
import os
import logging
from config import bot, dp
from phrases import get_text, lang_memory
from downloader import simultaneous, thumbnail, search_songs, clean_title, firstslice
logger = logging.getLogger(__name__)
title_memory = {}
search_memory = {}
memory = {}
photo_msg_memory = {}

@dp.message(Command("start"))
async def handle_message(message):
    keb = types.InlineKeyboardMarkup(inline_keyboard=[[
            types.InlineKeyboardButton(
               text = "Русский 🇷🇺", callback_data = "ru"),
            types.InlineKeyboardButton(
               text = "English 🇬🇧", callback_data = "en")
]])
    await message.answer(get_text("greeting", message.from_user.id), reply_markup = keb)

@dp.callback_query(F.data.in_(["ru", "en"]))
async def handle_language(callback):
    lang_memory[callback.from_user.id] = callback.data
    await callback.message.answer(get_text("lang_set", callback.from_user.id))

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
    
@dp.message(F.text)
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
        rows = [
            [types.InlineKeyboardButton(text="📹 360p", callback_data="360"),
            types.InlineKeyboardButton(text="📹 480p", callback_data="480")],
            [types.InlineKeyboardButton(text="📹 720p", callback_data="720"),
            types.InlineKeyboardButton(text="📹 1080p", callback_data="1080")],
            [types.InlineKeyboardButton(text="🎵 audio", callback_data="audio")],
]
        if "instagram.com" in message.text:
            rows.append([types.InlineKeyboardButton(text="📥 download audio", callback_data="download")])
        kb = types.InlineKeyboardMarkup(inline_keyboard=rows)

        sent_photo = await message.answer_photo(thumb_url, caption=info["title"], reply_markup = kb)
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
        header = get_text("Search_results", message.from_user.id)
        text = header + "\n\n" + text
        await message.answer(text, reply_markup = keyboard)


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
