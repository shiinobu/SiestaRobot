import html

from telegram.ext.filters import Filters
from telegram import Update, message, ParseMode
from telegram.ext import CallbackContext

from SiestaRobot.modules.helper_funcs.decorators import siestacmd, siestamsg
from SiestaRobot.modules.helper_funcs.channel_mode import user_admin, AdminPerms
from SiestaRobot.modules.sql.antichannel_sql import antichannel_status, disable_antichannel, enable_antichannel
from SiestaRobot.modules.language import gs

@siestacmd(command="antichannelmode", group=100)
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(text=gs(chat.id, "active_antichannel").format(html.escape(chat.title)))
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(text=gs(chat.id, "disable_antichannel").format(html.escape(chat.title)))
        else:
            message.reply_text(text=gs(chat.id, "invalid_antichannel").format(s))
        return
    message.reply_html(
        text=gs(chat.id, "status_antichannel").format(antichannel_status(chat.id), html.escape(chat.title)))

@siestamsg(Filters.chat_type.groups, group=110)
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot
    if not antichannel_status(chat.id):
        return
    if message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)
        
def helps(chat):
    return gs(chat, "antichannel_help")

__mod_name__ = "Anti-Channel"
