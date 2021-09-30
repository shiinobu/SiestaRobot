import codecs
import pickle
from asyncio import gather, get_running_loop
from io import BytesIO
from math import atan2, cos, radians, sin, sqrt
from random import randint
from re import findall
from time import time
from datetime import timedelta, datetime
from NaoRobot import aiohttpsession as aiosession
import aiofiles
import aiohttp
import speedtest
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pyrogram.types import Message
from wget import download

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image
