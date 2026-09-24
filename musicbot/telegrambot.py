from dotenv import load_dotenv
import asyncio
import logging
from logging_config import setup_logger
from config import bot, dp, tokenbot
from phrases import get_text, lang_memory
from downloader import thumbnail, simultaneous, search_songs, clean_title, firstslice
import handlers
load_dotenv()
setup_logger()

logger = logging.getLogger(__name__)

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

