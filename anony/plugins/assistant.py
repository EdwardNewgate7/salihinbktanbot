# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, lang, userbot


@app.on_message(filters.command(["assistant", "userbot", "assistants"]) & ~app.bl_users)
@lang.language()
async def _assistant_info(_, m: types.Message):
    if m.from_user.id not in app.sudoers:
        return await m.reply_text(m.lang.get("sudo_only", "This command is only for sudo users."))

    if not userbot.clients:
        return await m.reply_text(
            m.lang.get("assistant_none", "No assistants are running.")
        )

    lines = [m.lang.get("assistant_title", "Active assistants:")]
    for ub in userbot.clients:
        uname = f"@{ub.username}" if ub.username else "-"
        lines.append(f"• {ub.name} ({uname}) — <code>{ub.id}</code>")
    await m.reply_text("\n".join(lines))
