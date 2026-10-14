from dotenv import load_dotenv
import asyncio
import logging
from logging_config import setup_logger
from config import bot, dp
import handlers.choice_handler as choice_handler
import handlers.downloader as downloader
import handlers.language as language
import handlers.link_downloader as link_downloader
import handlers.start as start
import handlers.user_choice as user_choice
load_dotenv()
setup_logger()
dp.include_routers(start.router, downloader.router, choice_handler.router, language.router, link_downloader.router, user_choice.router)
logger = logging.getLogger(__name__)

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

