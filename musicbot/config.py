from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os

load_dotenv()

tokenbot = os.getenv("BOT_TOKEN")
bot = Bot(token=tokenbot)
dp = Dispatcher()