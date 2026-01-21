# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["groupinfo", "group"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _groupinfo(_, m: types.Message):
    await utils.maybe_delete_command(m)
    chat = await app.get_chat(m.chat.id)
    username = f"@{chat.username}" if chat.username else "-"
    members = chat.members_count or 0
    text = m.lang.get(
        "groupinfo",
        "Title: {0}\nUsername: {1}\nID: {2}\nMembers: {3}",
    ).format(chat.title, username, chat.id, members)
    await m.reply_text(text)
