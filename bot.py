import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ---------- НАСТРОЙКИ ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан! Добавь его в Environment на Render.")

WEBAPP_URL = "https://preeminent-frangipane-7041d3.netlify.app/webapp.html"

# Фразы для команды /scam (можешь добавить свои)
SCAM_LINES = [
    "Ой, меня на /scam позвали… у меня всего один навык: притворяться, что я взломал Пентагон 🛠",
    "Скам выполнен успешно. Пострадавших нет, урон нанесён только моей репутации.",
    "Внимание! Обнаружен скамер. Это я. Простите, боролся с голодом до зарплаты.",
    "Схема простая: скинул 100 рублей — получил 0 рублей. Так работает экономика.",
    "Не волнуйся, я не скамер. Я просто очень плохо шучу про скам.",
]

# ---------- ИНИЦИАЛИЗАЦИЯ ----------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- КЛАВИАТУРА ----------
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔗 Панелька", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    return builder.as_markup()

def who_called(message: Message) -> str:
    if message.from_user.username:
        return f"@{message.from_user.username}"
    return message.from_user.first_name or "друг"

# ---------- ОБРАБОТЧИКИ ----------
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text="👑 **Главное меню**\n\nНажми на кнопку ниже:",
        reply_markup=get_main_menu(),
        parse_mode="Markdown"
    )

@dp.message(Command("scam"))
async def cmd_scam(message: Message):
    # Отвечаем рандомной фразой, обращаясь к тому, кто вызвал
    await message.answer(f"{who_called(message)}, держи:\n{random.choice(SCAM_LINES)}")

# ---------- ЗАПУСК ----------
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
