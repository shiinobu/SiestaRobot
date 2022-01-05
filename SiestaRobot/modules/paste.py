import asyncio
import os
import re
import codecs
import requests
from io import BytesIO

import aiofiles
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext

from SiestaRobot import aiohttpsession as session
from SiestaRobot import pbot as app
from SiestaRobot.utils.errors import capture_err
from SiestaRobot.modules.helper_funcs.decorators import siestacmd
from SiestaRobot.utils.pastebin import paste
from SiestaRobot.modules.helper_funcs.alternate import typing_action

__mod_name__ = "Paste​"

pattern = re.compile(
    r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$"
)


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


@app.on_message(filters.command("paste") & ~filters.edited)
@capture_err
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply To A Message With /paste"
        )
    m = await message.reply_text("Pasting...")
    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
    elif message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.file_size > 1048576:
            return await m.edit(
                "You can only paste files smaller than 1MB."
            )
        if not pattern.search(document.mime_type):
            return await m.edit("Only text files can be pasted.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste(content)
    preview = link + "/preview.png"
    button = InlineKeyboard(row_width=1)
    button.add(InlineKeyboardButton(text="Paste Link", url=link))

    if await isPreviewUp(preview):
        try:
            await message.reply_photo(
                photo=preview, quote=False, reply_markup=button
            )
            return await m.delete()
        except Exception:
            pass
    return await m.edit(link)


@siestacmd(command="spaste")
@typing_action
def spacepaste(update, context):
    message = update.effective_message
    bot, args = context.bot, context.args

    if not message.reply_to_message.text:
        file = bot.getFile(message.reply_to_message.document)
        file.download("file.txt")
        text = codecs.open("file.txt", "r+", encoding="utf-8")
        paste_text = text.read()
        print(paste_text)
        os.remove("file.txt")

    elif message.reply_to_message.text:
        paste_text = message.reply_to_message.text
    elif len(args) >= 1:
        paste_text = message.text.split(None, 1)[1]

    else:
        message.reply_text(
            "reply to any message or just do /paste <what you want to paste>"
        )
        return

    extension = "txt"
    url = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            url, data={"content": paste_text, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}

    response = response.json()
    text = (
        f"**Pasted to [Space.bin]('https://spaceb.in/{response['payload']['id']}')!!!**"
    )
    buttons = [
        [
            InlineKeyboardButton(
                text="View Link", url=f"https://spaceb.in/{response['payload']['id']}"
            ),
            InlineKeyboardButton(
                text="View Raw",
                url=f"https://spaceb.in/api/v1/documents/{response['payload']['id']}/raw",
            ),
        ]
    ]
    message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
