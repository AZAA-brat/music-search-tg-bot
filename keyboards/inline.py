from keyboards.callbacks import QualityCB, AudioCB
from aiogram import types
from aiogram.types import InlineKeyboardMarkup

quality_kb = InlineKeyboardMarkup(inline_keyboard=[
     [types.InlineKeyboardButton(text="📹 480p", callback_data=QualityCB(quality=480).pack()),
    types.InlineKeyboardButton(text="📹 720p", callback_data=QualityCB(quality=720).pack())],
    [types.InlineKeyboardButton(text="🎵 audio", callback_data=AudioCB(audio="mp3").pack())]
]
)