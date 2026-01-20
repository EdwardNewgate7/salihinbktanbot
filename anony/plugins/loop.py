# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, db, lang
from anony.helpers import can_manage_vc, utils


@app.on_message(filters.command(["loop", "cloop"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _loop(_, m: types.Message):
    await utils.maybe_delete_command(m)
    if len(m.command) != 2:
        return await m.reply_text(m.lang.get("loop_usage", "Usage: /loop 1-10 | enable | disable"))

    state = m.command[1].strip().lower()
    if state.isnumeric():
        count = int(state)
        if not (1 <= count <= 10):
            return await m.reply_text(m.lang.get("loop_usage", "Usage: /loop 1-10 | enable | disable"))
        await db.set_loop(m.chat.id, count)
        return await m.reply_text(
            m.lang.get("loop_enabled", "Loop set to {0} by {1}").format(count, m.from_user.mention)
        )

    if state in ["enable", "on"]:
        await db.set_loop(m.chat.id, 10)
        return await m.reply_text(
            m.lang.get("loop_enabled", "Loop set to {0} by {1}").format("∞", m.from_user.mention)
        )
    if state in ["disable", "off"]:
        await db.set_loop(m.chat.id, 0)
        return await m.reply_text(
            m.lang.get("loop_disabled", "Loop disabled by {0}").format(m.from_user.mention)
        )

    return await m.reply_text(m.lang.get("loop_usage", "Usage: /loop 1-10 | enable | disable"))
