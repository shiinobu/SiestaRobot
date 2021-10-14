import re
import os

from telethon import events, Button
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from NaoRobot.events import register
from NaoRobot import telethn as tbot

PHOTO = "https://telegra.ph/file/b342fdfdfbb8e915231ed.jpg"
LOGO = "https://telegra.ph/file/f4ddca245f6f43cde3b9f.jpg"

@register(pattern=("/alive"))
async def awake(event):
  ken = event.sender.first_name
  TEXT = f"**Hi {ken}, I'm Nao Tomori.** \n\n"
  TEXT += "🌼 **I'm Working Properly** \n\n"
  TEXT += "🌼 **My Master : [Sena](https://t.me/xgothboi)** \n\n"
  TEXT += "🌼 **Python Version :** `3.9.7` \n\n"
  TEXT += f"🌼 **Telethon Version :** `{tlhver}` \n\n"
  TEXT += f"🌼 **Pyrogram Version :** `{pyrover}` \n\n"
  TEXT += "**Thanks For Adding Me Here ❤️**"
  BUTTON = [[Button.url("ʜᴇʟᴘ", "https://t.me/naoex_bot?start=help"), Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/kenbotsupport")]]
  await tbot.send_file(event.chat_id, PHOTO, caption=TEXT,  buttons=BUTTON)


@register(pattern=("/repo"))
async def repo(event):
  ken = event.sender.first_name
  TEXT = f"**Hi {ken}, I'm Nao Tomori.** \n\n"
  TEXT += "**My Master : [Sena](https://t.me/xgothboi)** \n\n"
  TEXT += "**If you wanna make your own bot, you can click the Source button bellow ❤️**"
  BUTTON = [[Button.url("sᴏᴜʀᴄᴇ​", "https://github.com/KennedyProject/NaoRobot"), Button.url("sᴜᴘᴘᴏʀᴛ", "https://t.me/kenbotsupport")]]
  await tbot.send_file(event.chat_id, LOGO, caption=TEXT,  buttons=BUTTON)
