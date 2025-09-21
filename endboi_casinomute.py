from datetime import timedelta
import asyncio
from aiogram import Bot, Dispatcher, types

API_TOKEN = "7402083428:AAFa1rAJrZecCuMKr1iX2ZXSq7SGdHRriJo"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_dice(message: types.Message):
    if message.dice:  # есть интерактивный emoji
        if message.dice.emoji == "🎰":  # это слот
            # Мутим пользователя на 15 минут
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

async def main():
    print("SlotDiceBot запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
