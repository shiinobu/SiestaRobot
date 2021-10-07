import os
import cv2
from PIL import Image
from NaoRobot.events import register
from NaoRobot import telethn as tbot


@register(pattern="^/tiny ?(.*)")
async def _(event):
    reply = await event.get_reply_message()
    if not (reply and(reply.media)):
       await event.reply("`Please reply to a sticker`")
       return
    xx = await event.edit("`Converting sticker to tiny`")
    ik = await tbot.download_media(reply)
    im1 = Image.open("NaoRobot/resources/man_black.png")
    if ik.endswitch(".tgs"):
        await event.tbot.download_media(reply, "man_black.tgs")
        os.system("lottie_convert.py man_black.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        jsn = jsn.replace("512", "2000")
        open = ("json.json", "w").write(jsn)
        os.system("lottie_convert.py json.json man_black.tgs")
        file = "man_black.tgs"
        os.remove("json.json")
    elif ik.endswitch((".gif", ".mp4")):
                iik = cv2.VideoCapture(ik)
        dani, busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await event.tbot.send_file(event.chat_id, file, reply_to=event.reply_to_msg_id)
    await xx.delete()
    os.remove(file)
    os.remove(ik)


__mod_name__="tiny"
