import yt_dlp
def simultaneous(link, options):
    with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(link)
            return info