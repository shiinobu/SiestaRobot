import sys
from pyrogram import Client
from pyrogram.session import SessionName
from NaoRobot.confing import get_int_key, get_str_key

STRING_SESSION = get_str_key("SESSION_STRING", required=True)
API_ID = get_int_key("API_ID", required=True)
API_HASH = get_str_key("API_HASH", required=True)

ubot = Client(SessionName(SESSION_STRING), API_ID, API_HASH)
try:
    ubot.start()
except BaseException:
    print("Userbot Error ! Have you added a SESSION_STRING in deploying??")
    sys.exit(1)
