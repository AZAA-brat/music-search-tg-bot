from aiogram.filters.callback_data import CallbackData

class QualityCB(CallbackData, prefix="quality"):
    quality: int

class PickCB(CallbackData, prefix="pick"):
    index: int

class AudioCB(CallbackData, prefix="audio"):
    audio: str

class ChoiceCB(CallbackData, prefix="choice"):
    choice: str