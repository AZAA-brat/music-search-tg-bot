# Music Search & Download Bot

A Telegram bot for downloading music and videos. Paste a link from YouTube, Instagram, or TikTok, or type a song name to search. The bot replies with a thumbnail and a quality picker, then sends the file.

The interface is in Russian by default, with an RU/EN language picker available on `/start`.

## Features

- **Link downloads:** Paste a YouTube, Instagram, or TikTok link to get a thumbnail and a quality choice: 360p, 480p, 720p, 1080p, or audio only.
- **Text search:** Type a song or artist name to see a numbered list of up to 10 matching results. Pick one to download it as audio.
- **Instagram audio:** Instagram links include a "download audio" button. The bot searches for the track using the post's caption, since captions are often generic and results can be imprecise.
- **Language support:** Russian and English, selectable on `/start`.
- **Clean chat:** Status and thumbnail messages are removed once the file is sent. Captions include the title, uploader, and a bot footer.

## Limitations

- Instagram audio search relies on caption text, not audio recognition, so matches are sometimes wrong.
- Photo-only Instagram posts aren't supported. The bot replies with a message saying so.
- Downloaded files and in-memory state are lost when the bot restarts.

## Tech Stack

- Python 3.10+
- [aiogram 3](https://docs.aiogram.dev/) for the Telegram bot framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for finding and downloading media
- [python-dotenv](https://pypi.org/project/python-dotenv/) for loading the `.env` file
- [ffmpeg](https://ffmpeg.org/) for converting audio and merging video (installed on the system, not via pip)

No database. State is kept in memory.

## Project Structure

```
music-search-tg-bot/
├── telegrambot.py        # Entry point: registers routers and starts polling
├── config.py             # Loads BOT_TOKEN and creates the Bot and Dispatcher
├── logging_config.py     # Logging setup
├── keyboards/            # All keyboard layouts, kept out of handlers
│   ├── callbacks.py      # Callback prefixes and data classes for inline buttons
│   ├── inline.py         # Inline keyboards: quality, search results, Instagram audio
│   └── reply.py          # Reply keyboards: language picker on /start
├── handlers/             # Telegram message and button handlers
│   ├── start.py          # /start and language picker
│   ├── language.py       # Saves the chosen language from the reply keyboard
│   ├── link_downloader.py  # Handles pasted links and text searches
│   ├── downloader.py     # Instagram "download audio" button
│   ├── choice_handler.py # Quality buttons (360p to 1080p, audio)
│   └── user_choice.py    # Picks a result from a search list
├── functions/            # Non-Telegram logic
│   ├── thumbnail.py      # Fetches a link's title and thumbnail
│   ├── search_engine.py  # Searches YouTube for up to 10 results
│   ├── extractor.py      # Downloads media with yt-dlp
│   ├── slicer.py         # Formats the result list text
│   └── cleaner.py        # Removes hashtags from titles
└── utils/
    ├── phrases.py        # RU/EN text strings and language lookup
    └── dictionaries.py   # In-memory state per user
```

## Setup

1. **Prerequisites:** Python 3.10 or newer, and ffmpeg installed and available on your `PATH`.

2. **Clone the repository:**

   ```bash
   git clone https://github.com/AZAA-brat/music-search-tg-bot.git
   cd music-search-tg-bot
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root:

   ```
   BOT_TOKEN=your_telegram_bot_token
   ```

   Get a token from [@BotFather](https://t.me/BotFather) on Telegram.

5. **Run the bot** from the project root, so the package imports resolve:

   ```bash
   python telegrambot.py
   ```

## Notes

- Downloaded files are saved to `downloads/`, which is excluded from git.
- Never commit `.env`. It is excluded by `.gitignore`.