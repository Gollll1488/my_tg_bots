import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Берем токен из настроек Render
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_main_menu():
    builder = InlineKeyboardBuilder()
    # Добавляем кнопку, которая открывает наше приложение
    # ВАЖНО: ссылка должна быть на реальный файл webapp.html на Render
    builder.row(
        InlineKeyboardButton(
            text="🚀 Открыть приложение", 
            web_app=WebAppInfo(url="https://my-tg-bots.onrender.com/webapp.html")
        )
    )
    builder.row(
        InlineKeyboardButton(text="📜 Команды", callback_data="commands")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text="👑 **Главное меню**\n\nНажми на кнопку ниже, чтобы открыть мини-приложение!",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "commands")
async def show_commands(callback):
    await callback.message.answer(
        "📜 **Доступные команды:**\n"
        "/start — Главное меню\n"
        "/scam — Вывести юзернейм\n"
    )
    await callback.answer()

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
