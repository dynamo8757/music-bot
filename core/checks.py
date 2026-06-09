from core.client import (
    app,
    assistant
)


async def is_assistant_in_chat(chat_id):

    try:

        me = await assistant.get_me()

        dialogs = []

        async for dialog in assistant.get_dialogs():
            dialogs.append(dialog.chat.id)

        return chat_id in dialogs

    except Exception as e:

        print(
            f"Assistant Check Error: {e}"
        )

        return False


async def get_assistant_username():

    try:

        me = await assistant.get_me()

        return me.username

    except Exception:

        return "Assistant"


async def is_voice_chat_active(chat_id):

    try:

        chat = await assistant.get_chat(
            chat_id
        )

        print(
            f"Voice Chat Check: {chat.title}"
        )

        return True

    except Exception as e:

        print(
            f"Voice Chat Check Error: {e}"
        )

        return False
    
async def auto_join_assistant(
    chat_id
):

    try:

        invite = await app.export_chat_invite_link(
            chat_id
        )

        await assistant.join_chat(
            invite
        )

        return True

    except Exception as e:

        print(
            f"Assistant Auto Join Error: {e}"
        )

        return False    