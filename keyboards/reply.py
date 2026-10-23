from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
rus = "Русский"
eng = "English"
lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=rus)],
        [KeyboardButton(text=eng)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)