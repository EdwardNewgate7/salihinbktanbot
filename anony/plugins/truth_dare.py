# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import httpx
from pyrogram import filters, types

from anony import app, lang

TRUTH_API = "https://api.truthordarebot.xyz/v1/truth"
DARE_API = "https://api.truthordarebot.xyz/v1/dare"


@app.on_message(filters.command(["truth"]) & ~app.bl_users)
@lang.language()
async def _truth(_, m: types.Message):
    try:
        async with httpx.AsyncClient(timeout=10.0) as http:
            res = await http.get(TRUTH_API)
        if res.status_code == 200:
            question = res.json().get("question", "No question found.")
            return await m.reply_text(
                m.lang.get("truth_text", "Truth:\n\n{0}").format(question)
            )
        return await m.reply_text(m.lang.get("truth_failed", "Failed to fetch truth."))
    except Exception:
        return await m.reply_text(m.lang.get("truth_error", "Error fetching truth."))


@app.on_message(filters.command(["dare"]) & ~app.bl_users)
@lang.language()
async def _dare(_, m: types.Message):
    try:
        async with httpx.AsyncClient(timeout=10.0) as http:
            res = await http.get(DARE_API)
        if res.status_code == 200:
            question = res.json().get("question", "No question found.")
            return await m.reply_text(
                m.lang.get("dare_text", "Dare:\n\n{0}").format(question)
            )
        return await m.reply_text(m.lang.get("dare_failed", "Failed to fetch dare."))
    except Exception:
        return await m.reply_text(m.lang.get("dare_error", "Error fetching dare."))
