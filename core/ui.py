from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def start_keyboard(
    bot_username,
):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🌙 Add Mizuki",
                    url=f"https://t.me/{bot_username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    "⚡ Features",
                    callback_data="features"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎵 Support",
                    url="https://t.me/YOUR_SUPPORT_GROUP"
                ),
                InlineKeyboardButton(
                    "📢 Updates",
                    url="https://t.me/YOUR_UPDATES_CHANNEL"
                )
            ]
        ]
    )

def player_keyboard(
    status="playing",
    autoplay=True,
    mode="queue",
    expanded=False
):

    main_row = [
        InlineKeyboardButton(
            "❤️",
            callback_data="like"
        ),

        InlineKeyboardButton(
            "⏸"
            if status == "playing"
            else "▶",
            callback_data=
            "pause"
            if status == "playing"
            else "resume"
        ),

        InlineKeyboardButton(
            "🔁"
            if mode == "queue"
            else "🔀"
            if mode == "shuffle"
            else "🔂",
            callback_data="mode"
        ),

        InlineKeyboardButton(
            "⏭",
            callback_data="skip"
        ),

        InlineKeyboardButton(
            "⏹",
            callback_data="stop"
        )
    ]

    keyboard = [
        main_row
    ]

    if not expanded:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⚙ Show Controls",
                    callback_data="show_controls"
                )
            ]
        )

    else:

        keyboard.extend(
            [
                [
                    InlineKeyboardButton(
                        "🔉",
                        callback_data="vol_down"
                    ),

                    InlineKeyboardButton(
                        "🔊",
                        callback_data="vol_up"
                    ),

                    InlineKeyboardButton(
                        "📜",
                        callback_data="queue"
                    ),

                    InlineKeyboardButton(
                        "♾️",
                        callback_data="autoplay"
                    ),
                    InlineKeyboardButton(
                        "➕",
                        callback_data="save_song"
                    )
                ],

                [
                    InlineKeyboardButton(
                        "⚙ Hide Controls",
                        callback_data="hide_controls"
                    )
                ]
            ]
        )

    return InlineKeyboardMarkup(
        keyboard
    )
def assistant_missing_text(username):

    return f"""
❌ **Assistant Missing**

Please add:

@{username}

to this group.

Then try again.
"""


VOICE_CHAT_MISSING = """
❌ No Active Voice Chat

Start a voice chat and try again.
"""


SEARCHING = """
🔍 Searching Song...
"""


DOWNLOADING = """
📥 Fetching Audio...
"""


JOINING = """
🎙 Joining Voice Chat...
"""


def now_playing(song_name):

    return f"""
🎵 **NOW PLAYING**

🎶 {song_name}

━━━━━━━━━━━━━━━

▶ Status: Playing

━━━━━━━━━━━━━━━

Use the buttons below to control playback.
"""


def added_to_queue(song_name, position):

    return f"""
📋 Added To Queue

🎶 {song_name}

Position: #{position}
"""


PAUSED = """
⏸ Music Paused
"""


RESUMED = """
▶ Music Resumed
"""


STOPPED = """
⏹ Music Stopped
"""


SKIPPED = """
⏭ Song Skipped
"""