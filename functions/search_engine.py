import yt_dlp
def search_songs(query, count=30):
    options = {"simulate": True}
    with yt_dlp.YoutubeDL(options) as yts:
        return yts.extract_info(f"ytsearch{count}:{query}")
