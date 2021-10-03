
import os
import shutil
import random, re
import glob
import time
import io
import requests
from io import BytesIO
from requests import get
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterPhotos
from NaoRobot.events import register
from NaoRobot import telethn as tbot


#Add telegraph media links of profile pics that are to be used
TELEGRAPH_MEDIA_LINKS = ["https://telegra.ph/file/b3da75d390da29a9c5145.jpg",
                         "https://telegra.ph/file/ae614f9fd0bbeba0350af.jpg",
                         "https://telegra.ph/file/08c5fbe14cc4b13d1de05.jpg",
                         "https://telegra.ph/file/66614a049d74fe2a220dc.jpg",
                         "https://telegra.ph/file/9cc1e4b24bfa13873bd66.jpg",
                         "https://telegra.ph/file/792d38bd74b0c3165c11d.jpg",
                         "https://telegra.ph/file/e1031e28a4aa4d8bd7c9b.jpg",
                         "https://telegra.ph/file/2be9027c55b5ed463fc18.jpg",
                         "https://telegra.ph/file/9fd71f8d08158d0cc393c.jpg",
                         "https://telegra.ph/file/627105074f0456f42058b.jpg",
                         "https://telegra.ph/file/62b712f741382d3c171cd.jpg",
                         "https://telegra.ph/file/496651e0d5e4d22b8f72d.jpg",
                         "https://telegra.ph/file/6619d0eee2c35e022ee74.jpg",
                         "https://telegra.ph/file/f72fcb27c9b1e762d184b.jpg",
                         "https://telegra.ph/file/01eac0fe1a722a864d7de.jpg",
                         "https://telegra.ph/file/bdcb746fbfdf38f812873.jpg",
                         "https://telegra.ph/file/d13e036a129df90651deb.jpg",
                         "https://telegra.ph/file/ab6715ce9a63523bd0219.jpg",
                         "https://telegra.ph/file/c243f4e80ebf0110f9f00.jpg",
                         "https://telegra.ph/file/ff9053f2c7bfb2badc99e.jpg",
                         "https://telegra.ph/file/00b9ebbb816285d9a59f9.jpg",
                         "https://telegra.ph/file/ad92e1c829d14afa25cf2.jpg",
                         "https://telegra.ph/file/58d45cc3374e7b28a1e67.jpg",
                         "https://telegra.ph/file/4140a0b3f27c302fd81cb.jpg",
                         "https://telegra.ph/file/c4db2b5c84c1d90f5ac8a.jpg",
                         "https://telegra.ph/file/c0da5080a3ff7643ddeb4.jpg",
                         "https://telegra.ph/file/79fad473ffe888ed771b2.jpg",
                         "https://telegra.ph/file/eafd526d9dcc164d7269f.jpg",
                         "https://telegra.ph/file/98b50e8424dd2be9fc127.jpg",
                         "https://telegra.ph/file/c1ad29c189162a1404749.jpg",
                         "https://telegra.ph/file/2d288450ebecc500addbd.jpg",
                         "https://telegra.ph/file/9715353976a99becd7632.jpg",
                         "https://telegra.ph/file/87670b02a1004bc02bd8d.jpg",
                         "https://telegra.ph/file/70789cd69114939a78242.jpg",
                         "https://telegra.ph/file/1566bd334f00645cfa993.jpg",
                         "https://telegra.ph/file/9727c37bb8c633208b915.jpg",
                         "https://telegra.ph/file/27467ef55fab117ccb278.jpg",
                         "https://telegra.ph/file/b9c62ff7810d9e84e9e2c.jpg",
                         "https://telegra.ph/file/87d22f2c95413059dda4e.jpg",
                         "https://telegra.ph/file/e528a731accbcdea140e3.jpg",
                         "https://telegra.ph/file/ee3f20c3ce71dc37fecb2.jpg",
                         "https://telegra.ph/file/a049f78377a5b8257294d.jpg",
                         "https://telegra.ph/file/54d22d39ea89423b7533f.jpg",
                         "https://telegra.ph/file/d90baa59b6fe2bc3091d3.jpg",
                         "https://telegra.ph/file/b9b3f80dc4635faaeb472.jpg",
                         "https://telegra.ph/file/d64be0a98f441a33d2aef.jpg",
                         "https://telegra.ph/file/e2c59ac97a900bab5ad7d.jpg",
                         "https://telegra.ph/file/41baf461b0a34f1a881a9.jpg",
                         "https://telegra.ph/file/8d4082052b4bd0a8cc862.jpg",
                         "https://telegra.ph/file/e7d6e0c511137ad67d843.jpg",
                         "https://telegra.ph/file/d7b97ea806d4a905b71c4.jpg",
                         "https://telegra.ph/file/6bec48ea2c96cf3d668a4.jpg",
                         "https://telegra.ph/file/aa64389b70e0de02d18c5.jpg",
                         "https://telegra.ph/file/2f75d964a59a3a4ae90e0.jpg",
                         "https://telegra.ph/file/f408df72c57cfc05e734f.jpg",
                         "https://telegra.ph/file/9d88d9dfb50106bc43c91.jpg",
                         "https://telegra.ph/file/a5a6e0f9d172fa386621e.jpg",
                         "https://telegra.ph/file/b0fc771c91409ee5cd4dc.jpg",
                         "https://telegra.ph/file/b0fc771c91409ee5cd4dc.jpg",
                         "https://telegra.ph/file/f75e59ebd4059f394479e.jpg",
                         "https://telegra.ph/file/fc0308f59023d0c997166.jpg",
                         "https://telegra.ph/file/7e1c04947f6afb6cdf25c.jpg",
                         "https://telegra.ph/file/6279bb4be7e48da194353.jpg",
                         "https://telegra.ph/file/616784fcd89f13e789685.jpg",
                         "https://telegra.ph/file/803e7dd9fafdb086bce4a.jpg",
                         "https://telegra.ph/file/d7338861b7f996ec9d40d.jpg",
                         "https://telegra.ph/file/828730cd4d73333eaf129.jpg",
                         "https://telegra.ph/file/36c9321161d49c4b3d671.jpg",
                         "https://telegra.ph/file/ebeae90b99fe482d11784.jpg",
                         "https://telegra.ph/file/70f38f92fe8d3060a31e4.jpg",
                         "https://telegra.ph/file/db12cf905f557487abc60.jpg",
                         "https://telegra.ph/file/0f9be531164c927ded8ec.jpg",
                         "https://telegra.ph/file/57fb7a6df3d666878c6f3.jpg",
                         "https://telegra.ph/file/242930d9f7aaa0b0729fd.jpg",
                         "https://telegra.ph/file/883f255792d2c2ebdd5f5.jpg",
                         "https://telegra.ph/file/36a9c0c26967edf90d42d.jpg",
                         "https://telegra.ph/file/03bdaf253c43fc97adbbe.jpg",
                         "https://telegra.ph/file/5826715ff0895a5321d2d.jpg",
                         "https://telegra.ph/file/9849b3940f063b065f4e3.jpg"
                         ]


@register(pattern="^/logo ?(.*)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if not quew:
        await event.reply('`Provide Some Text To Draw.`')
        return
 try:
    pesan = await event.reply('`Creating your logo....`')
    text = event.pattern_match.group(1)
    randc = random.choice(TELEGRAPH_MEDIA_LINKS)
    img = Image.open(io.BytesIO(requests.get(randc).content))
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./NaoRobot/resources/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 120)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=5, stroke_fill="black")
    fname="naorobot.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption="Made by @naoex_bot")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'Error, Report @kenbotsupport, {e}')
    


@register(pattern="^/wlogo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id == OWNER_ID:
        pass
    else:

        if not quew:
            await event.reply("Provide Some Text To Draw!")
            return
        else:
            pass
    await event.reply("Creating your logo...wait!")
    try:
        text = event.pattern_match.group(1)
        img = Image.open("./NaoRobot/resources/EXPUB.png")
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        pointsize = 500
        fillcolor = "white"
        shadowcolor = "blue"
        fnt = glob.glob("./NaoRobot/resources/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h*0.21)
        image_width, image_height = img.size
        draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
        x = (image_widthz-w)/2
        y= ((image_heightz-h)/2+6)
        draw.text((x, y), text, font=font, fill="white", stroke_width=5, stroke_fill="black")
        fname="naorobot.png"
        img.save(fname, "png")
        await tbot.send_file(event.chat_id, file=fname, caption="Made by @naoex_bot")         
        await pesan.delete()
        if os.path.exists(fname):
                os.remove(fname)
    except Exception as e:
       await event.reply(f'Error, Report @kenbotsupport, {e}')


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__mod_name__ = "Logo"
