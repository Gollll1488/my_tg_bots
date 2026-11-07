import asyncio
import logging
import os
import aiosqlite
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://preeminent-frangipane-7041d3.netlify.app/webapp.html"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ =====
async def init_db():
    async with aiosqlite.connect("secretary.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                date TEXT
            )
        """)
        await db.commit()

# ===== ГЛАВНОЕ МЕНЮ =====
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="🔗 Панелька", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    builder.row(
        InlineKeyboardButton(text="📝 Мои заметки", callback_data="my_notes"),
        InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_notes")
    )
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text="👑 **Режим Секретаря**\n\n"
             "Просто напиши мне любой текст, и я сохраню его как заметку.\n"
             "Нажми «Мои заметки», чтобы посмотреть всё, что ты записал.",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

# ===== СОХРАНЕНИЕ ЗАМЕТКИ =====
@dp.message(F.text & ~F.text.startswith("/"))
async def save_note(message: Message):
    user_id = message.from_user.id
    text = message.text
    date = datetime.now().strftime("%d.%m.%Y %H:%M")

    async with aiosqlite.connect("secretary.db") as db:
        await db.execute(
            "INSERT INTO notes (user_id, text, date) VALUES (?, ?, ?)",
            (user_id, text, date)
        )
        await db.commit()
    
    await message.answer(f"✅ Заметка сохранена!\n\n📅 {date}\n📝 {text}")

# ===== ПРОСМОТР ЗАМЕТОК =====
@dp.callback_query(F.data == "my_notes")
async def show_notes(callback):
    user_id = callback.from_user.id
    async with aiosqlite.connect("secretary.db") as db:
        async with db.execute(
            "SELECT text, date FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 10",
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall()

    if not rows:
        await callback.message.answer("📭 У тебя пока нет заметок. Напиши что-нибудь!")
    else:
        notes_text = "📝 **Твои последние заметки:**\n\n"
        for text, date in rows:
            notes_text += f"📅 *{date}*\n{text}\n\n"
        await callback.message.answer(notes_text, parse_mode="Markdown")
    
    await callback.answer()

# ===== ОЧИСТКА ЗАМЕТОК =====
@dp.callback_query(F.data == "clear_notes")
async def clear_notes(callback):
    user_id = callback.from_user.id
    async with aiosqlite.connect("secretary.db") as db:
        await db.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
        await db.commit()
    await callback.message.answer("🗑 Все твои заметки удалены!")
    await callback.answer()

# ===== КОМАНДА /scam =====
@dp.message(Command("scam"))
async def cmd_scam(message: Message):
    await message.answer("@morfinfuckk")

async def main():
    await init_db()  # Создаем базу при запуске
    print("Бот-секретарь запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
