from aiogram import types
from aiogram.types import InlineKeyboardButton

from keyboards.callbacks import PickCB
from utils.phrases import get_text
def firstslice(entries, user_id):
    text = ""
    buttons = []
    for i, e in enumerate(entries, 1):
        duration = e.get('duration') or 0
        title = e.get('title') or get_text("unknown", user_id)
        minutes = duration // 60
        seconds = duration % 60
        text += f"{i}. {e[title]} — {minutes}:{seconds:02d}\n"
        buttons.append(InlineKeyboardButton(text = str(i), callback_data = PickCB(index=i).pack()))
    rows = []
    for start in range(0, len(buttons), 5):
        row = buttons[start:start + 5]
        if row:
            rows.append(row)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=rows)
    return text, keyboard