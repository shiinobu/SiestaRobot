from telethon.errors.rpcerrorlist import YouBlockedUserError
from NaoRobot import telethn as tbot
from NaoRobot.events import register
from NaoRobot import ubot
from asyncio.exceptions import TimeoutError


@register(pattern="^/sg ?(.*)")
async def lastname(steal):
    await steal.reply("```Mengambil Informasi Pengguna Tersebut..```")
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await steal.edit("```Mohon Balas Ke Pesan Pengguna.```")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await steal.edit("```Balas Ke Pesan Pengguna Yang Sebenarnya.```")
        return
    await steal.edit("```Mohon Menunggu..```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                r = await conv.get_response()
                response = await conv.get_response()
            except YouBlockedUserError:
                await steal.reply(
                    "```Mohon Unblock @sangmatainfo_bot Dan Coba Lagi```"
                )
                return
            if r.text.startswith("Name"):
                respond = await conv.get_response()
                await steal.edit(f"`{r.message}`")
                await ubot.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id, respond.id]
                ) 
                return
            if response.text.startswith("No records") or r.text.startswith(
                "No records"
            ):
                await steal.edit("```Saya Tidak Menemukan Informasi Pengguna Ini, Pengguna Ini Belum Pernah Mengganti Nama Sebelumnya```")
                await ubot.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id]
                )
                return
            else:
                respond = await conv.get_response()
                await steal.edit(f"```{response.message}```")
            await ubot.delete_messages(
                conv.chat_id, [msg.id, r.id, response.id, respond.id]
            )
    except TimeoutError:
        return await steal.edit("`Saya Sedang Sakit Mohon Maaf`")
