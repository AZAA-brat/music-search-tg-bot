def safe_filename(title, max_length=100, default="audio"):
    forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in forbidden_chars:
        title = title.replace(char, '_')
    title = title.strip()
    if len(title) > max_length:
        title = title[:max_length]
        title = title.strip()
    if not title:
        title = default
    return title
