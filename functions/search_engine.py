import yt_dlp
def search_songs(query, count=30):
    options = {
        "simulate": True,
        "ignoreerrors": True,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(options) as yts:
        results = yts.extract_info(f"ytsearch{count}:{query}")
    if results and results.get("entries"):
        results["entries"] = [e for e in results["entries"] if e]
    return results