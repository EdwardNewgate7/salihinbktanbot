# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, db, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["vcinfo", "vcmembers"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _vcinfo(_, m: types.Message):
    await utils.maybe_delete_command(m)
    try:
        assistant = await db.get_assistant(m.chat.id)
        participants = await assistant.get_participants(m.chat.id)
        if not participants:
            return await m.reply_text(
                m.lang.get("vcinfo_empty", "No users found in voice chat.")
            )

        lines = [m.lang.get("vcinfo_title", "🎧 VC Members:")]
        for p in participants:
            try:
                user = await app.get_users(p.user_id)
                name = user.mention if user else f"<code>{p.user_id}</code>"
            except Exception:
                name = f"<code>{p.user_id}</code>"

            mute_status = "🔇" if p.muted else "👤"
            screen_status = "🖥️" if getattr(p, "screen_sharing", False) else ""
            volume_level = getattr(p, "volume", "N/A")
            info = f"{mute_status} {name} | 🎚️ {volume_level}"
            if screen_status:
                info += f" | {screen_status}"
            lines.append(info)

        lines.append(
            m.lang.get("vcinfo_total", "Total: {0}").format(len(participants))
        )
        await m.reply_text("\n".join(lines))
    except Exception as e:
        await m.reply_text(
            m.lang.get("vcinfo_error", "Failed to fetch VC info: {0}").format(type(e).__name__)
        )
