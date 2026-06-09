import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Missing environment variable: {name}"
        )

    return value


BOT_TOKEN = get_env("BOT_TOKEN")

API_ID = int(
    get_env("API_ID")
)

API_HASH = get_env(
    "API_HASH"
)

SESSION_STRING = os.getenv(
    "SESSION_STRING",
    ""
)

BOT_USERNAME = get_env(
    "BOT_USERNAME"
)

ASSISTANT_USERNAME = get_env(
    "ASSISTANT_USERNAME"
)

OWNER_ID = int(
    get_env("OWNER_ID")
)