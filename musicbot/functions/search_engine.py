import yt_dlp
def search_songs(query):
    ytsearch10 = {"simulate": True}
    with yt_dlp.YoutubeDL(ytsearch10) as yts:
        return yts.extract_info(f"ytsearch10:{query}")
