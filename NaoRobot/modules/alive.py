import os
import re

from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from NaoRobot import USERBOT_USERNAME as ubu
from NaoRobot.events import register
from NaoRobot import telethn as tbot


PHOTO = "https://telegra.ph/file/6353b230a00d04cf309b2.jpg"

@register(pattern=("/alive"))
async def awake(event):
  TEXT = f"**Hi [{event.sender.first_name}](tg://user?id={event.sender.id}), I'm Emiko Robot.** \n\n"
  TEXT += "⚪ **I'm Working Properly** \n\n"
  TEXT += f"⚪ **My Master : [No Name](https://t.me/{ubu})** \n\n"
  TEXT += f"⚪ **Library Version :** `{telever}`\n\n"
  TEXT += f"⚪ **Python Version :** `3.9.7` \n\n"
  TEXT += f"⚪ **Telethon Version :** `{tlhver}` \n\n"
  TEXT += f"⚪ **Pyrogram Version :** `{pyrover}` \n\n"
  TEXT += "**Thanks For Adding Me Here ❤️**"
  BUTTON = [[Button.url("Help", "https://t.me/EmiexRobot?start=help"), Button.url("Support", "https://t.me/emikosupport")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)
