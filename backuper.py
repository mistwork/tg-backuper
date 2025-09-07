import os
import logging
import asyncio
import tarfile
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile, Message
from aiogram.filters import Command
from dotenv import load_dotenv
from pathlib import Path


load_dotenv() 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHAT_ID = int(os.getenv("TELEGRAM_DEFAULT_CHAT_ID"))
BOT_TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN"))
RAW_PATHS = os.getenv("BACKUP_PATHS", "")
DATA_ROOT = Path("/data")
PATHS = sorted([str(p) for p in DATA_ROOT.iterdir() if p.exists()])
BACKUP_INTERVAL = int(os.getenv("BACKUP_INTERVAL"))
BACKUP_DIR = "/tmp"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply(f"Welcome!\nYour CHAT_ID: <code>{message.chat.id}</code>", parse_mode="HTML")

def make_backup(path: str) -> str:
    base_name = os.path.basename(path.rstrip("/"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = os.path.join(BACKUP_DIR, f"{base_name}_{timestamp}.tar.gz")

    with tarfile.open(archive_name, "w:gz") as tar:
        if os.path.exists(path):
            tar.add(path, arcname=base_name)
    return archive_name

async def send_backup():
    for path in PATHS:
        try:
            archive_path = make_backup(path)
            file_name = os.path.basename(path)
            file = FSInputFile(archive_path)
            await bot.send_document(chat_id=CHAT_ID, document=file, 
                                    caption=
                                    f"<b>✅ Backup has been successfully created</b>\n\n"
                                    f"<b>💾 File name:</b> {file_name}\n"
                                    f"<b>📅 Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", 
                                    parse_mode="HTML")
            print(f"[{datetime.now()}] Backup sent: {archive_path}", flush=True)
            os.remove(archive_path)
        except Exception as e:
            print(f"Backup error for {path}: {e}", flush=True)



async def scheduler():
    while True:
        await send_backup()
        await asyncio.sleep(BACKUP_INTERVAL)

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())