import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, BusinessConnection, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")
BUSINESS_TOKEN = os.getenv("BUSINESS_TOKEN")  # Добавь эту переменную на Render
WEBAPP_URL = "https://preeminent-frangipane-7041d3.netlify.app/webapp.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)  # Обычный бот для меню
business_bot = Bot(token=BUSINESS_TOKEN)  # Бизнес-бот для чатов

dp = Dispatcher()

# ===== ОБЫЧНОЕ МЕНЮ =====
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🔗 Панелька", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text="👑 **Главное меню**\n\nНажми на кнопку **«Панелька»**!",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# ===== ОБРАБОТКА БИЗНЕС-СООБЩЕНИЙ (/scam в чатах) =====
@dp.business_message(Command("scam"))
async def handle_business_scam(message: Message):
    # Отправляем ответ от твоего имени в тот же чат
    await business_bot.send_message(
        chat_id=message.chat.id,
        text="@morfinfuckk"
    )

async def main():
    print("Бот запущен (обычный и бизнес)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
