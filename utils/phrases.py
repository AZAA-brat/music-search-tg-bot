from utils.dictionaries import lang_memory

phrases = {
    "lang_set": {"ru": "Новый язык установлен успешно", "en": "New language set successfully!"},
    "greeting": {"ru": "Привет!", "en": "Hello!"},
    "search_results": {"ru": "Результаты поиска", "en": "Search results"},
    "bot_footer": {"ru": "Скачано через @adfadadbot", "en": "Downloaded with @adfadadbot"},
    "error_download": {"ru": "Не удалось скачать", "en": "Couldn't download"},
    "error_search": {"ru": "Ничего не найдено", "en": "Nothing found"},
    "error_photo_post": {"ru": "Похоже, это пост с фото — пока не поддерживается", "en": "This looks like a photo post — not supported yet"},
    "resend": {"ru": "Отправьте ссылку ещё раз", "en": "Resend the link"},
    "unknown": {"ru": "Неизвестный", "en": "Unknown"},
    "next": {"ru": "Следующий ➡️", "en": "Next ➡️"},
    "back": {"ru": "⬅️ Назад ", "en": "⬅️ Back"},
    "error_timeout": {"ru": "Процесс скачивания занял много времени", "en": "Took too long to download"}
}

def get_text(label, user_id):
    lang = lang_memory.get(user_id, "ru")
    return phrases[label][lang]