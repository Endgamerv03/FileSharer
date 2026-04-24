import os
import logging
from logging.handlers import RotatingFileHandler

# ──────────────────────────────────────────────────────────────
#  INTERNAL SETTINGS (no need to change these)
# ──────────────────────────────────────────────────────────────
LOG_FILE_NAME = "bot.log"
PORT = os.getenv("PORT", "8080")          # Choreo needs 8080
MSG_EFFECT = 5046509860389126442           # Telegram message effect ID, leave as is

# ──────────────────────────────────────────────────────────────
#  BOT CREDENTIALS  ← Get these from my.telegram.org + @BotFather
# ──────────────────────────────────────────────────────────────
SESSION  = os.getenv("SESSION", "mybot")  # Any simple name e.g. "mybot"
TOKEN    = os.getenv("TOKEN")             # From @BotFather
API_ID   = int(os.getenv("API_ID", "0")) # From my.telegram.org
API_HASH = os.getenv("API_HASH", "")     # From my.telegram.org
WORKERS  = int(os.getenv("WORKERS", "5")) # Leave as 5

# ──────────────────────────────────────────────────────────────
#  OWNER  ← Your personal Telegram user ID
# ──────────────────────────────────────────────────────────────
OWNER_ID = int(os.getenv("OWNER_ID", "0"))  # Get from @userinfobot

# ──────────────────────────────────────────────────────────────
#  DATABASE  ← MongoDB Atlas (free tier is fine)
# ──────────────────────────────────────────────────────────────
DB_URI  = os.getenv("DB_URI", "")   # Full MongoDB connection string
DB_NAME = os.getenv("DB_NAME", "filebot")  # Any name you want

# ──────────────────────────────────────────────────────────────
#  CHANNELS
# ──────────────────────────────────────────────────────────────

# Your PRIVATE storage channel ID (where files are stored)
# Must start with -100  e.g. -1001234567890
DB_CHANNEL = int(os.getenv("DB_CHANNEL", "0"))

# Force Subscribe Channel
# Format in env var: just the channel ID e.g. -1001234567890
# request_enabled = False means direct join (not join request)
# timer = 0 means no re-check timer
_fsub_raw = os.getenv("FSUB_CHANNEL", "")
if _fsub_raw:
    FSUBS = [[int(_fsub_raw), False, 0]]
else:
    FSUBS = []  # Leave empty if you don't want force subscribe

# ──────────────────────────────────────────────────────────────
#  BOT SETTINGS
# ──────────────────────────────────────────────────────────────

# Auto-delete timer in seconds (300 = 5 minutes)
AUTO_DEL = int(os.getenv("AUTO_DEL", "300"))

# Admin Telegram user IDs (comma separated in env var e.g. "123456,789012")
ADMINS = [
    int(x.strip())
    for x in os.getenv("ADMINS", "0").split(",")
    if x.strip().isdigit()
]

# Protect content — if True, users cannot forward files sent by bot
PROTECT = os.getenv("PROTECT", "True") == "True"

# Disable inline buttons on files — set False if you want buttons shown
DISABLE_BTN = os.getenv("DISABLE_BTN", "False") == "True"

# ──────────────────────────────────────────────────────────────
#  URL SHORTENER (optional — leave blank to disable)
# ──────────────────────────────────────────────────────────────
SHORT_URL = os.getenv("SHORT_URL", "")       # e.g. "linkshortify.com"
SHORT_API = os.getenv("SHORT_API", "")       # API key from your shortener
SHORT_TUT = os.getenv("SHORT_TUT", "")       # Tutorial link for users

# ──────────────────────────────────────────────────────────────
#  BOT MESSAGES  ← Customize these however you like
# ──────────────────────────────────────────────────────────────
MESSAGES = {
    # Shown when user first starts the bot
    # {first} = user's first name
    "START": "<b>Hey {first}! 👋\n\nI deliver files on demand.\nUse a shared link to receive your files.</b>",

    # Shown when user hasn't joined the force-sub channel yet
    "FSUB": "<b>⚠️ Hey!\n\nYour file is ready but you need to join our channel first.\nJoin now to get your files.</b>",

    # Shown when user sends /about
    "ABOUT": "<b>File Store Bot\n\nBuilt with Pyrogram\nDatabase: MongoDB</b>",

    # Shown when user sends any random message (not a command)
    "REPLY": "<b>Please use a valid file link to receive files.</b>",

    # Shown when URL shortener is used
    "SHORT_MSG": "<b>Hey {first}!\n\nYour link is ready. Click Open Link below.</b>",

    # Photo shown on /start  (direct image URL or leave empty string "" to disable)
    "START_PHOTO": "",

    # Photo shown on force-sub message (direct image URL or leave empty string "" to disable)
    "FSUB_PHOTO": "",

    "SHORT_PIC": "",
    "SHORT": ""
}

# ──────────────────────────────────────────────────────────────
#  LOGGER  (internal — do not change)
# ──────────────────────────────────────────────────────────────
def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
