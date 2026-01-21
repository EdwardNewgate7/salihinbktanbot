# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import httpx
from pyrogram import filters, types

from anony import app, config, lang

TMDB_BASE = "https://api.themoviedb.org/3"


@app.on_message(filters.command(["movie"]) & ~app.bl_users)
@lang.language()
async def _movie(_, m: types.Message):
    if not config.TMDB_API_KEY:
        return await m.reply_text(m.lang.get("movie_no_key", "TMDB API key is missing."))
    if len(m.command) < 2:
        return await m.reply_text(
            m.lang.get("movie_usage", "Usage: /movie Inception")
        )

    movie_name = " ".join(m.command[1:])
    status = await m.reply_text(m.lang.get("movie_search", "Searching..."))

    try:
        info = await _get_movie_info(movie_name)
        await status.edit_text(info)
    except Exception:
        await status.edit_text(m.lang.get("movie_failed", "Failed to fetch movie info."))


async def _get_movie_info(query: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        search = await client.get(
            f"{TMDB_BASE}/search/movie",
            params={"api_key": config.TMDB_API_KEY, "query": query},
        )
        search_data = search.json()
        if not search_data.get("results"):
            return lang.languages["en"].get("movie_not_found", "Movie not found.")

        movie = search_data["results"][0]
        movie_id = movie["id"]

        details = await client.get(
            f"{TMDB_BASE}/movie/{movie_id}",
            params={"api_key": config.TMDB_API_KEY},
        )
        details_data = details.json()

        cast = await client.get(
            f"{TMDB_BASE}/movie/{movie_id}/credits",
            params={"api_key": config.TMDB_API_KEY},
        )
        cast_data = cast.json()
        actors = ", ".join([a["name"] for a in cast_data.get("cast", [])[:5]]) or "N/A"

        title = details_data.get("title", "N/A")
        release = details_data.get("release_date", "N/A")
        overview = details_data.get("overview", "N/A")
        rating = details_data.get("vote_average", "N/A")
        revenue = details_data.get("revenue", 0)
        revenue_str = f"${revenue:,}" if revenue else "N/A"

        return (
            f"🎬 {title}\n"
            f"📅 {release}\n"
            f"⭐ {rating}/10\n"
            f"🎭 {actors}\n"
            f"💰 {revenue_str}\n\n"
            f"📝 {overview}"
        )
