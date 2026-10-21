from aiogram import types
from aiogram.types import InlineKeyboardButton

from keyboards.callbacks import PickCB, PageCB
from utils.phrases import get_text

PAGE_SIZE = 10
def firstslice(entries, user_id, page=1):
    start = (page-1) * PAGE_SIZE
    chunk = entries[start:start + PAGE_SIZE]
    text = ""
    buttons = []
    for i, e in enumerate(chunk, start + 1):
        duration = e.get('duration') or 0
        title = e.get('title') or get_text("unknown", user_id)
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        if duration >= 3600:
            text += f"{i}. {title} — {hours}:{minutes}:{seconds:02d}\n"
        else:
            text += f"{i}. {title} — {minutes}:{seconds:02d}\n"
        buttons.append(InlineKeyboardButton(text=str(i), callback_data=PickCB(index=i).pack()))
    for i, e in enumerate(entries, 1):
        duration = e.get('duration') or 0
        title = e.get('title') or get_text("unknown", user_id)
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        if duration >= 3600:
            text += f"{i}. {title} — {hours}:{minutes:02d}:{seconds:02d}\n"
        else:
            text += f"{i}. {title} — {minutes}:{seconds:02d}\n"
        buttons.append(InlineKeyboardButton(text = str(i), callback_data = PickCB(index=i).pack()))
    rows = []
    for start in range(0, len(buttons), 5):
        row = buttons[start:start + 5]
        if row:
            rows.append(row)
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=rows)
        return text, keyboard
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text=get_text("back", user_id), callback_data=PageCB(page=page - 1).pack()))
    if start + PAGE_SIZE < len(entries):
        nav.append(InlineKeyboardButton(text=get_text("next", user_id), callback_data=PageCB(page=page + 1).pack()))
    if nav:
        rows.append(nav)
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=rows)
    return text, keyboard