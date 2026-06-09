import time

from core.player_state import (
    song_start_times,
    paused_at,
    paused_duration,
    playback_status
)


def format_time(seconds):

    seconds = int(seconds)

    minutes = seconds // 60

    seconds = seconds % 60

    return f"{minutes}:{seconds:02d}"


def build_progress_bar(
    chat_id,
    duration
):
    start_time = song_start_times.get(
        chat_id,
        time.time()
    )

    total_paused = paused_duration.get(
        chat_id,
        0
    )

    if (
        playback_status.get(chat_id)
        == "paused"
        and
        chat_id in paused_at
    ):

        elapsed = int(
            paused_at[chat_id]
            - start_time
            - total_paused
        )

    else:

        elapsed = int(
            time.time()
            - start_time
            - total_paused
        )
        elapsed = min(
            elapsed,
            duration
        )

    filled = int(
        (elapsed / duration) * 10
    ) if duration > 0 else 0

    bar = (
        "▰" * filled
        +
        "▱" * (10 - filled)
    )

    return (
        f"{format_time(elapsed)} "
        f"{bar} "
        f"{format_time(duration)}"
    )