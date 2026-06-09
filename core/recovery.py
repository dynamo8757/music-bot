import traceback


async def safe_execute(
    coro,
    name="Task"
):

    try:

        await coro

        return True

    except Exception as e:

        print(
            f"❌ {name} Error: {e}"
        )

        return False