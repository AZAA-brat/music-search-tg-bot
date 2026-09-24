from dotenv import load_dotenv 
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import yt_dlp
import os
import asyncio

load_dotenv()

tokenbot = os.getenv("BOT_TOKEN")
title_memory = {}
lang_memory = {}
search_memory = {}
memory = {}
phrases = {
    "lang_set": {"ru": "Язык установлен", "en": "Language set"},
    "greeting": {"ru": "Привет!", "en": "Hello!"},
    "link_detected": {"ru": "Ссылка обнаружена", "en": "Link detected"},
    "Search_results": {"ru": "Результаты поиска", "en": "Search results"},
    "bot_footer": {"ru": "Скачано через @adfadadbot", "en": "Downloaded via @adfadadbot"},
}

def get_text(label, user_id):
    lang = lang_memory.get(user_id, "ru")
    return phrases[label][lang]
bot = Bot(token=tokenbot)
dp = Dispatcher()

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
        info = await asyncio.to_thread(thumbnail, message.text)
        title_memory[message.from_user.id] = info["title"]
        thumb_url = info["thumbnail"]
        memory[message.from_user.id] = message.text
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="📹 360p", callback_data="360"),
        types.InlineKeyboardButton(text="📹 480p", callback_data="480"),
    ],
    [
        types.InlineKeyboardButton(text="📹 720p", callback_data="720"),
        types.InlineKeyboardButton(text="📹 1080p", callback_data="1080"),
    ],
    [
        types.InlineKeyboardButton(text="🎵 audio", callback_data="audio"),
    ],
    [
        types.InlineKeyboardButton(text="📥 download audio", callback_data = "download") 
    ]
])
        await message.answer_photo(thumb_url, caption=info["title"], reply_markup = kb)
    else:
        results = await asyncio.to_thread(search_songs, message.text)
        result_url = results["entries"]
        search_memory[message.from_user.id] = result_url
        text, keyboard = firstslice(result_url[0:10])
        header = get_text("Search_results", message.from_user.id)
        text = header + "\n\n" + text
        await message.answer(text, reply_markup = keyboard)

def firstslice(entries):
    text = ""
    buttons = []
    for i, e in enumerate(entries, 1):
        minutes = e['duration'] // 60
        seconds = e['duration'] % 60
        text += f"{i}. {e['title']} — {minutes}:{seconds:02d}\n"
        buttons.append(InlineKeyboardButton(text = str(i), callback_data = str(i)))
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[buttons[0:5], buttons[5:10]])
    return text, keyboard

def search_songs(query):
    ytsearch10 = {"simulate": True}
    with yt_dlp.YoutubeDL(ytsearch10) as yts:
        return yts.extract_info(f"ytsearch10:{query}")
    
def simultaneous(link, options):
    with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(link)
            return info
    
def thumbnail(link):
    ydl_opts = {"simulate": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(link)

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
    info = await asyncio.to_thread(simultaneous, link, options)

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
    info = await asyncio.to_thread(simultaneous, link, options)
    if callback.data == "audio":
        path = f"downloads/{callback.from_user.id}.mp3"
        filename = types.FSInputFile(f"downloads/{callback.from_user.id}.mp3", filename=f"{info['title']}.mp3")
        caption = f"{info['title']}, {info.get('uploader', 'Неизвестный')}"
        await callback.message.answer_audio(filename, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}")
        await status_msg.delete()
        os.remove(path)
    else:
        path2 = f"downloads/{callback.from_user.id}.mp4"
        filename2 = types.FSInputFile(f"downloads/{callback.from_user.id}.mp4")
        caption = f"{info['title']}, {info.get('uploader', 'Неизвестный')}"
        await callback.message.answer_video(filename2, caption=caption + f"\n{get_text('bot_footer', callback.from_user.id)}")
        await status_msg.delete()
        os.remove(path2)

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

