# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import html
from datetime import datetime

import aiohttp
from pyrogram import filters, types
from pyrogram.enums import ParseMode

from anony import app, lang


def _safe(value: str | None) -> str:
    return html.escape(value or "")


def _short(text: str, limit: int = 350) -> str:
    text = text.strip()
    return (text[: limit - 1] + "...") if len(text) > limit else text


def _fmt_date(iso: str | None) -> str:
    if not iso:
        return "N/A"
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except Exception:
        return iso


@app.on_message(filters.command(["git", "github"]) & ~app.bl_users)
@lang.language()
async def _gitinfo(_, m: types.Message):
    if len(m.command) != 2:
        return await m.reply_text(
            m.lang.get("git_usage", "Usage: /git <username>")
        )

    username = m.command[1].strip()
    api = f"https://api.github.com/users/{username}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api, timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 404:
                    return await m.reply_text(m.lang.get("git_not_found", "User not found."))
                if r.status == 403:
                    return await m.reply_text(m.lang.get("git_rate", "Rate limit hit. Try again later."))
                if r.status != 200:
                    return await m.reply_text(
                        m.lang.get("git_error", "Failed to fetch data: {0}").format(r.status)
                    )
                data = await r.json()
    except Exception:
        return await m.reply_text(m.lang.get("git_failed", "Request failed."))

    name = _safe(data.get("name") or "Not specified")
    bio = _short(_safe(data.get("bio") or "No bio available."))
    blog_raw = (data.get("blog") or "").strip()
    blog_is_url = blog_raw.lower().startswith(("http://", "https://"))
    blog_disp = _safe(blog_raw) if blog_raw else "N/A"
    location = _safe(data.get("location") or "Unknown")
    company = _safe(data.get("company") or "N/A")
    created = _safe(_fmt_date(data.get("created_at")))
    profile_url = data.get("html_url") or ""
    repos = _safe(str(data.get("public_repos", "0")))
    followers = _safe(str(data.get("followers", "0")))
    following = _safe(str(data.get("following", "0")))
    avatar = data.get("avatar_url") or None

    if blog_is_url:
        blog_disp = f'<a href="{html.escape(blog_raw)}">{blog_disp}</a>'

    caption = (
        f"<b>{m.lang.get('git_title', 'GitHub Profile')}</b>\n\n"
        f"👤 <b>Name:</b> <code>{name}</code>\n"
        f"🔧 <b>Username:</b> <code>{_safe(username)}</code>\n"
        f"📌 <b>Bio:</b> {bio}\n"
        f"🏢 <b>Company:</b> {company}\n"
        f"📍 <b>Location:</b> {location}\n"
        f"🌐 <b>Blog:</b> {blog_disp}\n"
        f"🗓 <b>Created:</b> <code>{created}</code>\n"
        f"📁 <b>Repos:</b> <code>{repos}</code>\n"
        f"👥 <b>Followers:</b> <code>{followers}</code> | "
        f"<b>Following:</b> <code>{following}</code>\n"
        f"🔗 <b>Profile:</b> <a href=\"{html.escape(profile_url)}\">GitHub</a>"
    )

    if avatar:
        await m.reply_photo(
            photo=avatar,
            caption=caption,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    else:
        await m.reply_text(
            caption,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
