import asyncio

from core.client import app

from assistant import (
    start_assistant,
    stop_assistant
)

from core.vc_player import (
    start_pytgcalls
)

from core.tasks import (
    cleanup_task,
    health_logger,
    stats_saver,
    assistant_watchdog,
    progress_updater
)

from core.playlist_manager import (
    init_playlist_db
)

import handlers.start
import handlers.music
import handlers.controls
import handlers.callbacks
import handlers.queue
import handlers.nowplaying
import handlers.remove
import handlers.clearqueue
import handlers.stats
import handlers.health
import handlers.debug
import handlers.playlist
import handlers.download



async def main():

    print("\n" + "=" * 50)
    print("🎵 MIZUKI BOT")
    print("=" * 50)
    init_playlist_db()
    print("✅ Playlist Database Ready")

    try:

        await app.start()

        me = await app.get_me()

        print(
            f"🤖 Bot Logged In: @{me.username}"
        )

        assistant_ok = await start_assistant()

        if assistant_ok:
            await start_pytgcalls()

        if not assistant_ok:
            print(
                "⚠️ Assistant Login Failed"
            )

        print("✅ Ready")
        print("=" * 50)
        asyncio.create_task(cleanup_task())
        asyncio.create_task(health_logger())
        asyncio.create_task(stats_saver())
        asyncio.create_task(assistant_watchdog())
        asyncio.create_task(progress_updater())

        await asyncio.Event().wait()

    except Exception as e:
        print(
            f"❌ Startup Error: {e}"
        )

    finally:
        try:
            await stop_assistant()
        except Exception:
            pass

        try:
            await app.stop()
        except Exception:
            pass


if __name__ == "__main__":
    app.run(main())