from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os

load_dotenv()

tokenbot = os.getenv("BOT_TOKEN")
if not tokenbot:
    raise ValueError("BOT_TOKEN is missing\n"
                     "Add it to your .env file")
bot = Bot(token=tokenbot)
dp = Dispatcher()