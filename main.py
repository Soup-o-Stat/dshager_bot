import asyncio
import random
import os
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = "8488364373:AAENa3O_jh3C1IeRIC3QhLPyKs7RQ7UMBCA"
RESPONSE_CHANCE = 0.07
FILES_FOLDER = "videos"

bot = Bot(token=TOKEN)
dp = Dispatcher()

START_TIME = datetime.now(timezone.utc)

def get_random_file():
    try:
        files = [f for f in os.listdir(FILES_FOLDER) if os.path.isfile(os.path.join(FILES_FOLDER, f))]
        if not files:
            return None
        return os.path.join(FILES_FOLDER, random.choice(files))
    except FileNotFoundError:
        return None

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print("Send start message")
    await message.answer("Привет, я Джагернаут!\n"
                         "Я бот, который будет иногда отвечать на ваши сообщения забавными видео, фото и гифками!\n"
                         "Подписывайся на мой канал: https://t.me/dshager_channel\n"
                         "Ты можешь посмотреть список моих комманд, написал /help !")

@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    print("Send support message")
    await message.answer("Ты можешь поддержать меня тут: https://www.donationalerts.com/r/soup_o_stat")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    print("Sending help message")
    await message.answer("Список команд:\n"
                         "/start - приветственное сообщение\n"
                         "/support - поддержать меня\n"
                         "/send - отправка фото/видео/гиф\n"
                         "/help - список команд")

@dp.message(Command("send"))
async def cmd_send(message: types.Message):
    print("Sending send message")
    file_path = get_random_file()
    if file_path:
        ext = os.path.splitext(file_path)[1].lower()
        print(f">> Sending file: {file_path}, {message.date}, {message.message_id}")
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            await message.reply_photo(types.FSInputFile(file_path))
        elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
            await message.reply_video(types.FSInputFile(file_path))
        else:
            await message.reply_document(types.FSInputFile(file_path))

@dp.message()
async def handle_group(message: types.Message):
    msg_date = message.date
    if msg_date.tzinfo is None:
        msg_date = msg_date.replace(tzinfo=timezone.utc)
    if msg_date < START_TIME:
        print(f"Lost message (id={message.message_id}, date={msg_date})")
        return

    if random.random() < RESPONSE_CHANCE:
        file_path = get_random_file()
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            print(f">> Sending file: {file_path}, {message.date}, {message.message_id}")
            if ext in [".jpg", ".jpeg", ".png", ".webp"]:
                await message.reply_photo(types.FSInputFile(file_path))
            elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
                await message.reply_video(types.FSInputFile(file_path))
            else:
                await message.reply_document(types.FSInputFile(file_path))

async def main():
    print("Bot has been activated!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
