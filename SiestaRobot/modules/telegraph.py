import os

from SiestaRobot.events import register
from SiestaRobot import telethn as Client
from telethon import events, Button, types

TMP_DOWNLOAD_DIRECTORY = "./"

from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions


wibu = "SiestaRobot"
telegraph = Telegraph()
data = telegraph.create_account(short_name=wibu)
auth_url = data["auth_url"]


@register(pattern="^/t(gm|gt) ?(.*)")
async def telegrap(event):
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_msg = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "gm":
            downloaded_file_name = await Client.download_media(
                reply_msg,
                TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            if not downloaded_file_name:
                await Client.send_message(
                    event.chat_id,
                    "Not Supported Format Media!"
                )
                return
            else:
                if downloaded_file_name.endswith((".webp")):
                    resize_image(downloaded_file_name)
                try:
                    start = datetime.now()
                    media_urls = upload_file(downloaded_file_name)
                except exceptions.TelegraphException as exc:
                    await event.reply("ERROR: " + str(exc))
                    os.remove(downloaded_file_name)
                else:
                    end = datetime.now()
                    ms_two = (end - start).seconds
                    os.remove(downloaded_file_name)
                    await Client.send_message(
                        event.chat_id,
                        "Your telegraph is complete uploaded!",
                        buttons=[
                            [
                                types.KeyboardButtonUrl(
                                    "➡ View Telegraph", "https://telegra.ph{}".format(media_urls[0], (ms + ms_two))
                                )
                            ]
                        ]
                    )
        elif input_str == "gt":
            user_object = await Client.get_entity(reply_msg.sender_id)
            title_of_page = user_object.first_name # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = reply_msg.message
            if reply_msg.media:
                if page_content != "":
                    title_of_page = page_content
                else:
                    await Client.send_message(
                        event.chat_id,
                        "Not Supported Format Text!"
                    )
                downloaded_file_name = await Client.download_media(
                    reply_msg,
                    TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await Client.send_message(
                    event.chat_id,
                    "Your telegraph is complete uploaded!",
                    buttons=[
                        [
                            types.KeyboardButtonUrl(
                                "➡ View Telegraph", "https://telegra.ph/{}".format(response["path"], ms)
                            )
                        ]
                    ]
                )
    else:
        await event.reply("Reply to a message to get a permanent telegra.ph link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__mod_name__ = "Telegraph"
