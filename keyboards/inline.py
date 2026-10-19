from keyboards.callbacks import QualityCB, AudioCB, ChoiceCB
from aiogram import types
from aiogram.types import InlineKeyboardMarkup

quality_kb = InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="📹 360p", callback_data=QualityCB(quality=360).pack()),
     types.InlineKeyboardButton(text="📹 480p", callback_data=QualityCB(quality=480).pack())],
    [types.InlineKeyboardButton(text="📹 720p", callback_data=QualityCB(quality=720).pack()),
     types.InlineKeyboardButton(text="📹 1080p", callback_data=QualityCB(quality=1080).pack())],
    [types.InlineKeyboardButton(text="🎵 audio", callback_data=AudioCB(audio="mp3").pack())]
]
)
choice_kb = InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Focus music", callback_data=ChoiceCB(choice="focus_music").pack()),
     types.InlineKeyboardButton(text="Lofi music", callback_data=ChoiceCB(choice="lofi_music").pack())],
    [types.InlineKeyboardButton(text="Vibe music", callback_data=ChoiceCB(choice="vibe_music").pack()),
     types.InlineKeyboardButton(text="Deephouse music", callback_data=ChoiceCB(choice="deephouse_music").pack())],
]
)