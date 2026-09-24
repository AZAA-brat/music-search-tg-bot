lang_memory = {}

phrases = {
    "lang_set": {"ru": "Язык установлен", "en": "Language set"},
    "greeting": {"ru": "Привет!", "en": "Hello!"},
    "link_detected": {"ru": "Ссылка обнаружена", "en": "Link detected"},
    "Search_results": {"ru": "Результаты поиска", "en": "Search results"},
    "bot_footer": {"ru": "Скачано через @adfadadbot", "en": "Downloaded via @adfadadbot"},
    "error_download": {"ru": "Не удалось скачать", "en": "Couldn't download"},
    "error_search": {"ru": "Ничего не найдено", "en": "Nothing found"},
    "error_link": {"ru": "Ссылка недействительна", "en": "Invalid link"},
    "error_photo_post": {"ru": "Похоже, это пост с фото — пока не поддерживается", "en": "This looks like a photo post — not supported yet"}
}

def get_text(label, user_id):
    lang = lang_memory.get(user_id, "ru")
    return phrases[label][lang]