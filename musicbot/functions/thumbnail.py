import yt_dlp
def thumbnail(link):
    ydl_opts = {"simulate": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(link)