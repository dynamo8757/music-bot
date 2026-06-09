from pyrogram import filters

from core.client import app

from core.vc_player import (
    pause_music,
    resume_music,
    stop_music,
    skip_music
)

from core.ui import (
    PAUSED,
    RESUMED,
    STOPPED,
    SKIPPED
)


@app.on_message(filters.command("pause"))
async def pause_command(client, message):

    try:

        ok = await pause_music(
            message.chat.id
        )

        if ok:

            await message.reply_text(
                PAUSED
            )

        else:

            await message.reply_text(
                "❌ Nothing is playing."
            )

    except Exception as e:

        await message.reply_text(
            f"❌ {e}"
        )


@app.on_message(filters.command("resume"))
async def resume_command(client, message):

    try:

        ok = await resume_music(
            message.chat.id
        )

        if ok:

            await message.reply_text(
                RESUMED
            )

        else:

            await message.reply_text(
                "❌ Nothing is paused."
            )

    except Exception as e:

        await message.reply_text(
            f"❌ {e}"
        )


@app.on_message(filters.command("stop"))
async def stop_command(client, message):

    try:

        await stop_music(
            message.chat.id
        )

        await message.reply_text(
            STOPPED
        )

    except Exception as e:

        await message.reply_text(
            f"❌ {e}"
        )


@app.on_message(filters.command("skip"))
async def skip_command(client, message):

    try:

        next_song = await skip_music(
            message.chat.id
        )

        if next_song:

            await message.reply_text(
                f"⏭ Skipped\n\n🎵 {next_song['song']['title']}"
            )

        else:

            await message.reply_text(
                SKIPPED
            )

    except Exception as e:

        await message.reply_text(
            f"❌ {e}"
        )