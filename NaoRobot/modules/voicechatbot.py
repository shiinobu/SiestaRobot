# Voics Chatbot Module Credits Pranav Ajay 🐰Github = Red-Aura 🐹 Telegram= @madepranav
# @lyciachatbot support Now
import os
import aiofiles
import aiohttp
from random import randint
from pyrogram import filters
from NaoRobot import pbot as Nao


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data


async def ai_Nao(url):
    ai_name = "Naotomori.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ai_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return ai_name


@Nao.on_message(filters.command("voice"))
async def Nao(_, message):
    if len(message.command) < 2:
        await message.reply_text("Nao Tomori AI Voice Chatbot")
        return
    text = message.text.split(None, 1)[1]
    Nao = text.replace(" ", "%20")
    m = await message.reply_text("Nao Is Best...")
    try:
        L = await fetch(
            f"https://api.affiliateplus.xyz/api/chatbot?message={nao}&botname=@NaoTomori_Robot&ownername=@xgothboi&user=1"
        )
        chatbot = L["message"]
        VoiceAi = f"https://lyciavoice.herokuapp.com/nao?text={chatbot}&lang=id"
        name = "nao"
    except Exception as e:
        await m.edit(str(e))
        return
    await m.edit("Made By @xgothboi")
    NaoVoice = await ai_Nao(VoiceAi)
    await m.edit("Repyping...")
    await message.reply_audio(audio=NaoVoice, title=chatbot, performer=name)
    os.remove(NaoVoice)
    await m.delete()
