import os
import io
import requests
import shutil 
import random
import re
import time
from requests import get
from NaoRobot.events import register
from NaoRobot import telethn

APAKAH_STRING = ["Iya", 
                 "Tidak", 
                 "Mungkin", 
                 "Mungkin Tidak", 
                 "Bisa jadi", 
                 "Mungkin Tidak",
                 "Tidak Mungkin",
                 "Pala bapak kau pecah",
                 "Apakah kamu yakin?",
                 "Tanya aja sama mamak au tu pler"
                 ]


@register(pattern="^/apakah ?(.*)")
async def apakah(event):
    quew = event.pattern_match.group(1)
    if not quew:
        await event.reply('Berikan pertanyaan yang spesifik...')
        return
    await event.reply(random.choice(APAKAH_STRING))
