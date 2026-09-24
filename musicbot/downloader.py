import yt_dlp
from aiogram import types
from aiogram.types import InlineKeyboardButton

def clean_title(caption):
    words = caption.split()
    kept = [w for w in words if not w.startswith("#")]
    return " ".join(kept)

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