from core.client import assistant


async def start_assistant():
    try:

        await assistant.start()

        me = await assistant.get_me()

        print(
            f"✅ Assistant Logged In: @{me.username}"
        )

        return True

    except Exception as e:

        print(
            f"❌ Assistant Login Failed: {e}"
        )

        return False


async def stop_assistant():
    try:

        await assistant.stop()

        print(
            "🛑 Assistant Stopped"
        )

    except Exception as e:

        print(
            f"❌ Assistant Stop Error: {e}"
        )