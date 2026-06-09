from core.client import app

from core.admin_cache import (
    get_cached_admins,
    set_cached_admins
)


async def is_admin(
    chat_id,
    user_id
):

    try:

        admins = get_cached_admins(
            chat_id
        )

        if admins is None:

            admins = []

            async for member in app.get_chat_members(
                chat_id,
                filter="administrators"
            ):
                admins.append(
                    member.user.id
                )

            set_cached_admins(
                chat_id,
                admins
            )

        return user_id in admins

    except Exception as e:

        print(
            f"Admin Check Error: {e}"
        )

        return False