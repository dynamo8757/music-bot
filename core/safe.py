import asyncio

from pyrogram.errors import (
    FloodWait
)


async def safe_call(
    coro
):

    try:

        return await coro

    except FloodWait as e:

        print(
            f"⏳ FloodWait {e.value}s"
        )

        await asyncio.sleep(
            e.value
        )

        return None

    except Exception as e:

        print(
            f"Safe Call Error: {e}"
        )

        return None