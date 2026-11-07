import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ---------- Настройки ----------

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN 9287103860:AAGUCq8H6LS4l_YMYUzlpJ3zbLrMREj077A"
        "BOT_TOKEN=9287103860:AAGUCq8H6LS4l_YMYUzlpJ3zbLrMREj077A python bot.py"
    )

WEBAPP_URL = "https://preeminent-frangipane-7041d3.netlify.app/webapp.html"

# Заготовки для /scam — можешь дописать свои
SCAM_LINES = [
    "Ой, меня на /scam позвали… у меня всего один навык: притворяться, "
    "что я взломал Пентагон 🛠",
    "Скам выполнен успешно. Пострадавших нет, урон нанесён только моей репутации.",
    "Внимание! Обнаружен скамер. Это я. Простите, боролся с голодом до зарплаты.",
    "Схема простая: скинул 100 рублей — получил 0 рублей. Так работает экономика.",
]

# ---------- Инициализация ----------

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔗 Панелька", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    return builder.as_markup()


def who_called(message: Message) -> str:
    """Имя того, кто вызвал команду: юзернейм или имя."""
    if message.from_user.username:
        return f"@{message.from_user.username}"
    return message.from_user.first_name or "друг"


# ---------- Хэндлеры ----------

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👑 Главное меню", reply_markup=get_main_menu())


@dp.message(Command("scam"))
async def cmd_scam(message: Message):
    # Бот отвечает от своего имени, подкалывая автора команды
    await message.answer(f"{who_called(message)}, держи:\n{random.choice(SCAM_LINES)}")


# ---------- Запуск ----------

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
