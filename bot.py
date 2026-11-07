import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Берем только обычный токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://preeminent-frangipane-7041d3.netlify.app/webapp.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔗 Панелька", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👑 **Главное меню**", reply_markup=get_main_menu(), parse_mode="Markdown")

# Обычная команда /scam (работает, если бот добавлен в группу или через секретаря)
@dp.message(Command("scam"))
async def cmd_scam(message: Message):
    await message.answer("@morfinfuckk")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
