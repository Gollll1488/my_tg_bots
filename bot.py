import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# ===== ТВОЙ ТОКЕН =====
BOT_TOKEN = "9287103860:AAFSUfIQn8aV8NxVLjCSArUhJXdMrWUXaHA"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Добрый денек, {message.from_user.first_name}! ☀️\n\n"
                         "Доступные команды:\n"
                         "/start — запуск\n"
                         "/scam — вывести юзернейм")

@dp.message(Command("scam"))
async def cmd_scam(message: Message):
    await message.answer("@morfinfuckk")

@dp.message(F.text)
async def echo_all(message: Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")