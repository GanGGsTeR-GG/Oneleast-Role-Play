import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")
DB_PATH = os.getenv("DB_PATH", "/code/data/db/game.db")
