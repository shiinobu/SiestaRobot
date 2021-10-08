import os
from asyncio.exceptions import TimeoutError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from NaoRobot.events import register
from NaoRobot import ubot
from NaoRobot import telethn as tbot
from NaoRobot import TEMP_DOWNLOAD_DIRECTORY


@register(pattern="^/kamuii ?(.*)")
async def _(event):
    try:
        level = fry.pattern_match.group(2)
        feri = await event.reply("`Deepfrying this image....`")
        async with ubot.conversation("@image_deepfrybot") as conv:
            try:
                query1 = await conv.send_message(f"/deepfry {level}")
                r = await conv.get_response()
                await ubot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await feri.edit("`Emrorr lol`")
            if r.text.startswith("No"):
                return await feri.edit(f"`Cannot find the image`")
            img = await ubot.download_media(r)
            await feri.edit("`Sending Image....`")
            await tbot.send_file(
                event.chat_id,
                img,
                force_document=False,
                reply_to=feri,
            )
            await feri.delete()
            await ubot.delete_messages(
                conv.chat_id, [r.id, query1.id]
            )
        os.system("rm *.png *.jpg")
    except TimeoutError:
        return await feri.edit("`Cannot find the image`")
