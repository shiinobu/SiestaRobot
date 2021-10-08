import re
import os

from telethon import events, Button
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from NaoRobot.events import register
from NaoRobot import telethn as tbot

PHOTO = "https://telegra.ph/file/b342fdfdfbb8e915231ed.jpg"

@register(pattern=("/alive"))
async def awake(event):
  ken = event.sender.first_name
  TEXT = f"**Hi {ken}, I'm Nao Tomori.** \n\n"
  TEXT += "🌼 **I'm Working Properly** \n\n"
  TEXT += "🌼 **My Master : [Sena](https://t.me/xgothboi)** \n\n"
  TEXT += "🌼 **Python Version :** `3.9.7`
  TEXT += f"🌼 **Telethon Version :** `{tlhver}` \n\n"
  TEXT += f"🌼 **Pyrogram Version :** `{pyrover}` \n\n"
  TEXT += "**Thanks For Adding Me Here ❤️**"
  BUTTON = [[Button.url("ʜᴇʟᴘ", "https://t.me/naoex_bot?start=help"), Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/kenbotsupport")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
