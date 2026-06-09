import asyncio

from core.cache import (
    audio_cache,
    search_cache
)

from core.player_state import (
    current_songs,
)



from core.player_card import (
    refresh_player_card
)

from core.client import app
from core.vc_player import active_chats
from core.player_state import stats
from core.stats_storage import save_stats
from core.client import assistant

async def cleanup_task():

    while True:

        try:

            # Keep only latest 500 entries
            while len(audio_cache) > 500:
                audio_cache.popitem(
                    last=False
                )

            while len(search_cache) > 500:
                search_cache.popitem(
                    last=False
                )

            print(
                f"🧹 Cache Cleanup | "
                f"Audio={len(audio_cache)} "
                f"Search={len(search_cache)}"
            )

        except Exception as e:

            print(
                f"Cleanup Error: {e}"
            )

        await asyncio.sleep(
            1800
        )
        

async def health_logger():

    while True:

        try:

            print(
                f"💚 HEALTH | "
                f"Chats={len(active_chats)}"
            )

        except Exception as e:

            print(
                f"Health Logger Error: {e}"
            )

        await asyncio.sleep(
            600
        )

async def stats_saver():

    while True:

        try:

            save_stats(
                stats
            )

            print(
                "💾 Stats Saved"
            )

        except Exception as e:

            print(
                f"Stats Save Error: {e}"
            )

        await asyncio.sleep(
            300
        )

async def assistant_watchdog():

    while True:

        try:

            me = await assistant.get_me()

            print(
                f"🤖 Assistant Alive: @{me.username}"
            )

        except Exception as e:

            print(
                f"⚠ Assistant Issue: {e}"
            )

        await asyncio.sleep(
            300
        )        

async def progress_updater():

    while True:

        try:

            for chat_id in list(
                current_songs.keys()
            ):

                song = current_songs[
                    chat_id
                ]["song"]

                requested_by = current_songs[
                    chat_id
                ]["requested_by"]

                await refresh_player_card(
                    chat_id,
                    song,
                    requested_by
                )

        except Exception as e:

            print(
                f"Progress Updater Error: {e}"
            )

        await asyncio.sleep(10)