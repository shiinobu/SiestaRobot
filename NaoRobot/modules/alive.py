import os
import re

from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from NaoRobot.events import register
from NaoRobot import telethn as tbot


PHOTO = "https://telegra.ph/file/f2a2b4937a55d250fd918.jpg"

@register(pattern=("/alive"))
async def awake(event):
  ken = event.sender.first_name
  TEXT = f"**Hi {ken}, I'm Nao Tomori.** \n\n"
  TEXT += "🌼 **I'm Working Properly** \n\n"
  TEXT += "🌼 **My Master : [Sena](https://t.me/xgothboi)** \n\n"
  TEXT += f"🌼 **Library Version :** `{telever}`\n\n"
  TEXT += f"🌼 **Python Version :** `3.9.7` \n\n"
  TEXT += f"🌼 **Telethon Version :** `{tlhver}` \n\n"
  TEXT += f"🌼 **Pyrogram Version :** `{pyrover}` \n\n"
  TEXT += "**Thanks For Adding Me Here ❤️**"
  BUTTON = [[Button.url("Help", "https://t.me/naoex_bot?start=help"), Button.url("Support", "https://t.me/kenbotsupport")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
