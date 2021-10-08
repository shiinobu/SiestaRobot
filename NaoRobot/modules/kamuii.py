import os
from asyncio.exceptions import TimeoutError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from NaoRobot.events import register
from NaoRobot import ubot
from NaoRobot import telethn as tbot
from NaoRobot import TEMP_DOWNLOAD_DIRECTORY


@register(pattern="^/wall ?(.*)")
async def _(fry):
    x = await fry.edit("`Deepfying this sticker`")
    level = fry.pattern_match.group(2)
    if fry.fwd_from:
        return
    if not fry.reply_to_msg_id:
        await k.edit("`Please reply to a sticker`")
        return
    reply_message = await fry.get_reply_message()
    if not reply_message.media:
        await k.edit("`image not supported`")
        return
    if reply_message.sender.bot:
        await fry.edit("`please reply to a sticker`")
        return
    chat = "@image_deepfrybot"
    message_id_to_reply = fry.message.reply_to_msg_id
    async with ubot.conversation("@image_deepfrybot") as conv:
            try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/deepfry {level}"
                msg_level = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await x.reply("`Please unblock`  @image_deepfrybot`...`")
            return
        if response.text.startswith("Forward"):
            await x.edit("`Please Turn Off Privacy Forward Settings...`")
        else:
            downloaded_file_name = await ubot.download_media(
                response.media,
                TEMP_DOWNLOAD_DIRECTORY
            )
            await tbot.send_file(
                fry.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply
            )
            """ - cleanup chat after completed - """
            try:
                msg_level
            except NameError:
                await ubot.delete_messages(conv.chat_id,
                                                 [msg.id, response.id])
            else:
                await fry.client.delete_messages(
                    conv.chat_id,
                    [msg.id, response.id, r.id, msg_level.id])
    await x.delete()
    return os.remove(downloaded_file_name)


__mod_name__="kamuii"
