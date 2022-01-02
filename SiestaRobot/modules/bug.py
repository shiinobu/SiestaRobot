# SPDX-License-Identifier: MIT
# Copyright (c) 2018-2022 Amano Team

import re
from html import escape
from datetime import datetime

from pyrogram import (
    Client,
    Filters,
)
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from telegram.ext import (
    CommandHandler,
    run_async,
)

from SiestaRobot.config import BUG_LOG

async def bug (cln:Client, msg:Message):
    if len(msg.text.split()) > 1:
        try:
            datetime_fmt = "%H:%M - %d-%m-%Y"
            bug_report = (
                "<b>#BUG</b>\n"
                f"User: {msg.from_user.mention}\n"
                f"ID: <code>{msg.from_user.id}</code>\n\n"
                "The content of the report:\n"
                f"<code>{escape(msg.text.split(None, 1)[1])}</code>\n"
                f"<b>Event Stamp</b>: <code>{datetime.utcnow().strftime(datetime_fmt)}</code>"
            )
            await cln.send_message(
                chat_id=BUG_LOG,
                text=bug_report,
                disable_web_page_preview=True,
            )
            await msg.reply_text(f"The bug was successfully reported to the support group")
        except BadRequest:
            await msg.reply_text(f"The bug was failed reported to the support group")
    else:
        await msg.reply(f"No bug to report")

__mod_name__ = "Bug"

BUG_HANDLER = CommandHandler(["bug"], bug, filters=Filters.chat_type.groups, run_async=True)