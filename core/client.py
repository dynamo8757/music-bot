from pyrogram import Client

from config.settings import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    SESSION_STRING
)


app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    no_updates=True
)