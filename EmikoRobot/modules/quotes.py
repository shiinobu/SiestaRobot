from io import BytesIO
from traceback import format_exc

from pyrogram import filters
from pyrogram.types import Message

from EmikoRobot import arq
from EmikoRobot.utils.errors import capture_err
from EmikoRobot import pbot as app


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message: Message) -> bool:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@app.on_message(filters.command("q"))
@capture_err
async def quotly_func(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to quote it."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Replied message has no text, can't quote it."
        )
    warna = event.pattern_match.group(1)
    chat = "@QuotLyBot"
    m = await message.reply_text("Quoting Messages Please wait....")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            first = await conv.send_message(f"/qcolor {warna}")
            ok = await conv.get_response()
            await asyncio.sleep(2)
            second = await bot.forward_messages(chat, reply_message)
            response = await response
    else:
        await m.edit(
            "Incorrect argument, check quotly module in help section."
        )
        return
    try:
        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit(
            "Something wrong happened while quoting messages,"
            + " This error usually happens when there's a "
            + " message containing something other than text."
        )
        e = format_exc()
        print(e)


__mod_name__ = "Quotly"
