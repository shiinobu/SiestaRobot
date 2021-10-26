import html
import random
import NaoRobot.modules.apakah_string as apakontol_string
from NaoRobot import dispatcher
from telegram import ParseMode, Update, Bot
from NaoRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async


def apakah(update: Update, context: CallbackContext):
    args = context.args
    update.effective_message.reply_text(random.choice(apakontol_string.APAKAH))


APAKAH_HANDLER = DisableAbleCommandHandler("apakah", apakah, run_async=True)

dispatcher.add_handler(APAKAH_HANDLER)
