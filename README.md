# Telegram Backup Bot
## About the Project ℹ️

**Telegram Backup Bot** is a simple tool for automating backups of files and directories to your Telegram chat.

- 🗂️ Backup any files or directories: Just specify paths in the .env file.
- ⏱️ Scheduled backups: Automatic backup at a configurable interval (seconds).
- 📤 Send backups via Telegram: Archives are sent directly to your specified Telegram chat.
- 🐳 Docker-ready: Easily run in Docker with dynamic volume mounting.

## Installation & Running 🛠️

1. Clone the project:
```bash
git clone https://github.com/mistwork/tg-backuper.git
```
2. Go to project folder:
```bash
cd tg-backuper
```
3. Create a `.env` file in the project root:
```bash
nano .env
```
Contents of the `.env` file:
```env
# Telegram Settings
TELEGRAM_BOT_TOKEN=your_bot_token # Your Telegram bot token
TELEGRAM_DEFAULT_CHAT_ID=your_chat_id # Your Telegram ID

# Backup Settings
BACKUP_PATHS=your_backup_paths # Example: /home/user/backuping_file.txt,/home/user/backuping_dir
BACKUP_INTERVAL=3600 # Backup interval in seconds (e.g., 3600 = 1 hour)
```

4. Generate custom `docker-compose.yml` file:
```bash
python3 generate_compose.py
```
5. Run:
```bash
docker compose up -d --build
```

To view logs:
```bash
docker compose logs -f
```

To stop the service:
```bash
docker compose down
```

### How to create Telegram Bot:

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the provided bot token