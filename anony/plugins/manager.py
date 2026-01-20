# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import enums, filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["id", "info"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _id_info(_, m: types.Message):
    await utils.maybe_delete_command(m)
    user = await utils.extract_user(m) or m.from_user
    if m.command[0] == "id":
        if m.reply_to_message and m.reply_to_message.from_user:
            return await m.reply_text(
                m.lang.get("id_user", "User ID: {0}").format(user.id)
            )
        return await m.reply_text(
            m.lang.get("id_chat", "Chat ID: {0}").format(m.chat.id)
        )

    name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "-"
    text = m.lang.get(
        "info_user",
        "Name: {0}\nUsername: {1}\nID: {2}",
    ).format(name or "-", username, user.id)
    return await m.reply_text(text)


@app.on_message(filters.command(["purge", "del"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _purge(_, m: types.Message):
    await utils.maybe_delete_command(m)
    if not m.reply_to_message:
        return await m.reply_text(
            m.lang.get("purge_usage", "Reply to a message to purge.")
        )
    start = m.reply_to_message.id
    end = m.id
    deleted = 0
    for msg_id in range(start, end):
        try:
            await app.delete_messages(m.chat.id, msg_id)
            deleted += 1
        except Exception:
            continue
    await m.reply_text(
        m.lang.get("purge_done", "Purged {0} messages.").format(deleted)
    )


@app.on_message(filters.command(["promote", "demote", "kick"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _admin_actions(_, m: types.Message):
    await utils.maybe_delete_command(m)
    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang.get("user_not_found", "User not found."))

    if m.command[0] == "kick":
        try:
            await app.ban_chat_member(m.chat.id, user.id)
            await app.unban_chat_member(m.chat.id, user.id)
            return await m.reply_text(
                m.lang.get("kick_done", "User kicked: {0}").format(user.mention)
            )
        except Exception:
            return await m.reply_text(
                m.lang.get("kick_failed", "I couldn't kick that user.")
            )

    if m.command[0] == "promote":
        try:
            await app.promote_chat_member(
                m.chat.id,
                user.id,
                can_manage_chat=True,
                can_change_info=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_manage_video_chats=True,
            )
            return await m.reply_text(
                m.lang.get("promote_done", "User promoted: {0}").format(user.mention)
            )
        except Exception:
            return await m.reply_text(
                m.lang.get("promote_failed", "I couldn't promote that user.")
            )

    if m.command[0] == "demote":
        try:
            await app.promote_chat_member(
                m.chat.id,
                user.id,
                can_manage_chat=False,
                can_change_info=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_manage_video_chats=False,
            )
            return await m.reply_text(
                m.lang.get("demote_done", "User demoted: {0}").format(user.mention)
            )
        except Exception:
            return await m.reply_text(
                m.lang.get("demote_failed", "I couldn't demote that user.")
            )
