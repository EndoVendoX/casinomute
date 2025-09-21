from datetime import timedelta
import asyncio
from aiogram import Bot, Dispatcher, types
import os
import threading
from flask import Flask
import random  # опционально для логов keep-alive

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
if not API_TOKEN:
    raise ValueError("API_TOKEN пустой! Проверь Environment Variables в Render")

# Эмодзи, за которые мутим
FORBIDDEN_EMOJIS = ["🎰", "⚽", "🏀", "🎲", "🎯", "🎳"]

@dp.message()
async def handle_dice(message: types.Message):
    if message.dice:
        emoji = message.dice.emoji
        if any(emoji.startswith(e) for e in FORBIDDEN_EMOJIS):
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                permissions=types.ChatPermissions(can_send_messages=False),
                until_date=message.date + timedelta(minutes=30)
            )
            await message.reply(
                f"{message.from_user.first_name}, ну чтож ты за лудоман. Получай 30 минут мута."
            )
            print(f"Мут: {message.from_user.full_name}, слот: {message.dice.value}")

# --- keep-alive через мини Flask сервер ---
app = Flask("keep_alive")

@app.route("/")
def home():
    return "ok"

def run_web():
    app.run(host="0.0.0.0", port=10000)

# запускаем Flask в отдельном потоке
threading.Thread(target=run_web).start()
# --------------------------------------------

async def keep_alive_logs():
    # Дополнительно можно логировать случайные числа, чтобы видеть, что задача жива
    while True:
        print("Keep-alive tick:", random.randint(1,100))
        await asyncio.sleep(300)  # каждые 5 минут

async def on_startup():
    # Запускаем keep_alive_logs параллельно с polling
    asyncio.create_task(keep_alive_logs())

async def main():
    print("SlotDiceBot запущен...")
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    asyncio.run(main())



