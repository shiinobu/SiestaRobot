import sys
from pyrogram import TelegramClient
from pyrogram.sessions import StringSession
from NaoRobot.confing import get_int_key, get_str_key

STRING_SESSION = get_str_key("SESSION_STRING", required=True)
API_ID = get_int_key("API_ID", required=True)
API_HASH = get_str_key("API_HASH", required=True)

ubot = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
try:
    ubot.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)
