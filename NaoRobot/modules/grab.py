from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from NaoRobot import ubot2
from NaoRobot.events import register

@register(pattern="^/grab ?(.*)")
async def gpoto(e):
    kontol = e.pattern_match.group(0)
    a = await e.reply("`Getting this person pfp`")
    if kontol:
        pass
    elif e.is_reply:
        gs = await e.get_reply_message()
        kontol = gs.sender_id
    else:
        kontol = e.chat_id
    okla = await ubot2.download_profile_photo(kontol)
    if not okla:
        return await a.edit(a, "`Pfp Not Found...`")
    await a.delete()
    await e.reply(file=okla)
    os.remove(okla)
