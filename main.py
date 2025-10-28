import asyncio
import random
import os
import sys
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from termcolor import cprint

RESPONSE_CHANCE = 0.3
FILES_FOLDER = "videos"
START_TIME = datetime.now(timezone.utc)

def get_random_file():
    try:
        files = [f for f in os.listdir(FILES_FOLDER) if os.path.isfile(os.path.join(FILES_FOLDER, f))]
        if not files:
            return None
        return os.path.join(FILES_FOLDER, random.choice(files))
    except FileNotFoundError:
        return None

async def bot_loop(token):
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        cprint(f"[BOT]: {message.text}", "light_yellow")
        await message.answer(
            "Привет, я Джагернаут!\n"
            "Я бот, который будет иногда отвечать на ваши сообщения забавными видео, фото и гифками!\n"
            "Я эффективен в чатах, добавляй меня скорее --> @dshager_bot\n"
            "Подписывайся на мой канал: https://t.me/dshager_channel\n"
            "Ты можешь посмотреть список моих комманд, написав /help !"
        )

    @dp.message(Command("support"))
    async def cmd_support(message: types.Message):
        cprint(f"[BOT]: {message.text}", "light_yellow")
        await message.answer("Ты можешь поддержать меня тут: https://dalink.to/soup_o_stat")

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        cprint(f"[BOT]: {message.text}", "light_yellow")
        await message.answer(
            "Список команд:\n"
            "/start - приветственное сообщение\n"
            "/support - поддержать меня\n"
            "/send - отправка фото/видео/гиф\n"
            "/help - список команд"
        )

    @dp.message(Command("send"))
    async def cmd_send(message: types.Message):
        cprint(f"[BOT]: {message.text}", "light_yellow")
        file_path = get_random_file()
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            cprint(f">> Sending file: {file_path}, {message.date}, {message.message_id}", "light_green")
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
            cprint(f"Lost message (id={message.message_id}, date={msg_date})", "yellow")
            return

        if random.random() < RESPONSE_CHANCE:
            file_path = get_random_file()
            if file_path:
                ext = os.path.splitext(file_path)[1].lower()
                cprint(f">> Sending file: {file_path}, {message.date}, {message.message_id}", "light_green")
                if ext in [".jpg", ".jpeg", ".png", ".webp"]:
                    await message.reply_photo(types.FSInputFile(file_path))
                elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
                    await message.reply_video(types.FSInputFile(file_path))
                else:
                    await message.reply_document(types.FSInputFile(file_path))

    cprint("Bot has been activated!", "green")
    await dp.start_polling(bot)

async def listen_exit():
    while True:
        cmd = await asyncio.to_thread(input, "")
        if cmd.strip().lower() == "exit":
            cprint("Exit command received. Shutting down...", "red")
            exit()
        if cmd.strip().lower() == "clear":
            cprint("Clearing the console...", "red")
            if os.name == 'nt':
                _ = os.system('cls')
            else:
                _ = os.system('clear')
        if cmd.strip().lower == "chance":
            cprint(f"Chance: {RESPONSE_CHANCE}", "yellow")

async def main():
    if len(sys.argv) < 2:
        cprint("Error: no API token!", "red")
        sys.exit(1)

    token = sys.argv[1].strip()
    await asyncio.gather(bot_loop(token), listen_exit())

if __name__ == "__main__":
    asyncio.run(main())
