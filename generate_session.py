from pyrogram import Client
from pyrogram.errors import RPCError

print("\n" + "=" * 50)
print("🎵 MAHI MUSIC BOT")
print("🔑 SESSION STRING GENERATOR")
print("=" * 50)

API_ID = int(input("Enter API_ID: "))
API_HASH = input("Enter API_HASH: ")

try:
    app = Client(
        "session_generator",
        api_id=API_ID,
        api_hash=API_HASH
    )

    with app:
        session_string = app.export_session_string()

        me = app.get_me()

        print("\n" + "=" * 50)
        print("✅ Login Successful")
        print(f"👤 Name: {me.first_name}")

        if me.username:
            print(f"📛 Username: @{me.username}")

        print("\n🔑 SESSION STRING:\n")
        print(session_string)

        print("\n" + "=" * 50)
        print("Copy this string into:")
        print("SESSION_STRING=YOUR_STRING")
        print("inside your .env file")
        print("=" * 50)

except RPCError as e:

    print(
        f"\n❌ Telegram Error:\n{e}"
    )

except Exception as e:

    print(
        f"\n❌ Unexpected Error:\n{e}"
    )