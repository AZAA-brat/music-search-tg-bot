def audio_options(user_id):
    options = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
    }],
    "outtmpl": f"downloads/{user_id}",
}
    return options

def video_options(user_id, quality):
    options = {"format": f"bestvideo[height<={quality}]+bestaudio/best",
               "outtmpl": f"downloads/{user_id}.%(ext)s"}
    return options