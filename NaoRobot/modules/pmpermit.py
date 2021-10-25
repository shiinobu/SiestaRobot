from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory

from NaoRobot import BOT_ID, USERBOT_ID, USERBOT_PREFIX, pbot, ubot2, eor
from NaoRobot.ex_plugins.errors import capture_err
from NaoRobot.ex_plugins.dbfunctions import (approve_pmpermit, disapprove_pmpermit,
                                   is_pmpermit_approved)

flood = {}


@ubot2.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(USERBOT_ID)
)
@capture_err
async def pmpermit_func(_, message):
    user_id = message.from_user.id
    if await is_pmpermit_approved(user_id):
        return
    async for m in ubot2.iter_history(user_id, limit=6):
        if m.reply_markup:
            await m.delete()
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 5:
        await message.reply_text("SPAM DETECTED, BLOCKED USER AUTOMATICALLY!")
        return await ubot2.block_user(user_id)
    results = await ubot2.get_inline_bot_results(BOT_ID, f"pmpermit {user_id}")
    await ubot2.send_inline_bot_result(
        user_id,
        results.query_id,
        results.results[0].id,
        hide_via=True,
    )


@ubot2.on_message(
    filters.command("approve", prefixes=USERBOT_PREFIX)
    & filters.user(USERBOT_ID)
    & ~filters.via_bot
)
@capture_err
async def pm_approve(_, message):
    if not message.reply_to_message:
        return await eor(message, text="Reply to a user's message to approve.")
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        return await eor(message, text="User is already approved to pm")
    await approve_pmpermit(user_id)
    await eor(message, text="User is approved to pm")


@ubot2.on_message(
    filters.command("disapprove", prefixes=USERBOT_PREFIX)
    & filters.user(USERBOT_ID)
    & ~filters.via_bot
)
async def pm_disapprove(_, message):
    if not message.reply_to_message:
        return await eor(message, text="Reply to a user's message to approve.")
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await eor(message, text="User is already disapproved to pm")
        async for m in app2.iter_history(user_id, limit=6):
            if m.reply_markup:
                try:
                    await m.delete()
                except Exception:
                    pass
        return
    await disapprove_pmpermit(user_id)
    await eor(message, text="User is disapproved to pm")


@ubot2.on_message(
    filters.command("block", prefixes=USERBOT_PREFIX)
    & filters.user(USERBOT_ID)
    & ~filters.via_bot
) 
@capture_err
async def block_user_func(_, message):
    if not message.reply_to_message:
        return await eor(message, text="Reply to a user's message to block.")
    user_id = message.reply_to_message.from_user.id
    # Blocking user after editing the message so that other person can get the update.
    await eor(message, text="Successfully blocked the user")
    await ubot2.block_user(user_id)


@ubot2.on_message(
    filters.command("unblock", prefixes=USERBOT_PREFIX)
    & filters.user(USERBOT_ID)
    & ~filters.via_bot
)
async def unblock_user_func(_, message):
    if not message.reply_to_message:
        return await eor(message, text="Reply to a user's message to unblock.")
    user_id = message.reply_to_message.from_user.id
    await ubot2.unblock_user(user_id)
    await eor(message, text="Successfully Unblocked the user")


# CALLBACK QUERY HANDLER

flood2 = {}


@pbot.on_callback_query(filters.regex("pmpermit"))
async def pmpermit_cq(_, cq):
    user_id = cq.from_user.id
    data, victim = (
        cq.data.split(None, 2)[1],
        cq.data.split(None, 2)[2],
    )
    if data == "approve":
        if user_id != USERBOT_ID:
            return await cq.answer("This Button Is Not For You")
        await approve_pmpermit(int(victim))
        return await pbot.edit_inline_text(
            cq.inline_message_id, "User Has Been Approved To PM."
        )

    if data == "block":
        if user_id != USERBOT_ID:
            return await cq.answer("This Button Is Not For You")
        await cq.answer()
        await pbot.edit_inline_text(
            cq.inline_message_id, "Successfully blocked the user."
        )
        await ubot2.block_user(int(victim))
        return await ubot2.send(
            DeleteHistory(
                peer=(await ubot2.resolve_peer(victim)),
                max_id=0,
                revoke=False,
            )
        )

    if user_id == USERBOT_ID:
        return await cq.answer("It's For The Other Person.")

    if data == "to_scam_you":
        async for m in ubot2.iter_history(user_id, limit=6):
            if m.reply_markup:
                await m.delete()
        await ubot2.send_message(user_id, "Blocked, Go scam someone else.")
        await ubot2.block_user(user_id)
        await cq.answer()

    elif data == "approve_me":
        await cq.answer()
        if str(user_id) in flood2:
            flood2[str(user_id)] += 1
        else:
            flood2[str(user_id)] = 1
        if flood2[str(user_id)] > 5:
            await ubot2.send_message(user_id, "SPAM DETECTED, USER BLOCKED.")
            return await ubot2.block_user(user_id)
        await ubot2.send_message(
            user_id,
            "I'm busy right now, will approve you shortly, DO NOT SPAM.",
        )
