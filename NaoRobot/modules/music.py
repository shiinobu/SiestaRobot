import asyncio
import io
import os
import time
import requests
import wget
from pyrogram import filters
from pyrogram.types import Message
from tswift import Song
from youtube_dl import YoutubeDL
from youtubesearchpython import SearchVideos
from NaoRobot.utils.pluginhelper import get_text, progress
from NaoRobot import pbot, arq

async def lyrics_func(answers, text):
    song = await arq.lyrics(text)
    if not song.ok:
        answers.append(
            InlineQueryResultArticle(
                title="Error",
                description=song.result,
                input_message_content=InputTextMessageContent(
                    song.result
                ),
            )
        )
        return answers
    lyrics = song.result
    song = lyrics.splitlines()
    song_name = song[0]
    artist = song[1]
    if len(lyrics) > 4095:
        lyrics = await hastebin(lyrics)
        lyrics = f"**LYRICS_TOO_LONG:** [URL]({lyrics})"

    msg = f"{lyrics}"

    answers.append(
        InlineQueryResultArticle(
            title=song_name,
            description=artist,
            input_message_content=InputTextMessageContent(msg),
        )
    )
    return answers


@pbot.on_message(filters.command(["vsong", "video"]))
async def ytmusic(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**Video Name ➠** [{thum}]({mo}) \n**Requested For :** `{urlissed}` \n**Channel :** `{thums}` "
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {urlissed} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


@pbot.on_message(filters.command(["music", "song"]))
async def ytmusic(client, message: Message):
    urlissed = get_text(message)
    if not urlissed:
        await client.send_message(
            message.chat.id,
            "Invalid Command Syntax, Please Check Help Menu To Know More!",
        )
        return
    pablo = await client.send_message(
        message.chat.id, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    mio[0]["duration"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    sedlyf = wget.download(kekme)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(mo, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**Song Name :** [{thum}]({mo}) \n**Requested For :** `{urlissed}` \n**Channel :** `{thums}` "
    file_stark = f"{ytdl_data['id']}.mp3"
    await client.send_audio(
        message.chat.id,
        audio=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=sedlyf,
        caption=capy,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uploading {urlissed} Song From YouTube Music!`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


@pbot.on_message(filters.command(["lyric", "lyrics"]))
async def lyrics_func(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:**\n/lyrics [QUERY]")
    m = await message.reply_text("**Searching**")
    query = message.text.strip().split(None, 1)[1]
    song = await arq.lyrics(query)
    lyrics = song.result
    if len(lyrics) < 4095:
        return await m.edit(f"{lyrics}")
    lyrics = await paste(lyrics)
    await m.edit(f"**LYRICS_TOO_LONG:** [URL]({lyrics})")
