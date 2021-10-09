import html
import random
import NaoRobot.modules.spillgame_string as spill_string
from NaoRobot import dispatcher
from telegram import ParseMode, Update, Bot
from NaoRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async


def spill(update: Update, context: CallbackContext):
    args = context.args
    update.effective_message.reply_text(random.choice(spill_string.SPILL))


DARE_HANDLER = DisableAbleCommandHandler("spill", spill, run_async=True)

dispatcher.add_handler(SPILL_HANDLER)
