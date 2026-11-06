import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

9287103860:AAGUCq8H6LS4l_YMYUzlpJ3zbLrMREj077A


BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем кнопки
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔗 Панелька", url="https://t.me/ваша_ссылка"),
        InlineKeyboardButton(text="📜 Команды", callback_data="commands")
    )
    builder.row(
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👑 **Главное меню**\n\n"
        "Добро пожаловать! Выберите действие ниже:"
    )
    
    # Отправляем только текст с кнопками
    await message.answer(
        text=text,
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "commands")
async def show_commands(callback):
    await callback.message.answer(
        "📜 **Доступные команды:**\n"
        "/start — Главное меню\n"
        "/scam — Вывести юзернейм\n"
        "/time — Текущее время"
    )
    await callback.answer()

@dp.callback_query(F.data == "profile")
async def show_profile(callback):
    user = callback.from_user
    await callback.message.answer(
        f"👤 **Ваш профиль:**\n"
        f"ID: `{user.id}`\n"
        f"Имя: {user.first_name}\n"
        f"Юзернейм: @{user.username if user.username else 'нет'}"
    )
    await callback.answer()

@dp.message(Command("scam"))
async def cmd_scam(message: Message):
    await message.answer("@morfinfuckk")

@dp.message(Command("time"))
async def cmd_time(message: Message):
    from datetime import datetime
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await message.answer(f"🕐 Сейчас: {now}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
