from aiogram import types
from aiogram.types import InlineKeyboardButton
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