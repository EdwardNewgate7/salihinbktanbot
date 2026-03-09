# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic


import json
from functools import wraps
from pathlib import Path

from pyrogram import errors

from anony import db, logger

lang_codes = {
    "ar": "Arabic",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "ja": "Japanese",
    "my": "Burmese",
    "pa": "Punjabi",
    "pt": "Portuguese",
    "ru": "Russian",
    "tr": "Turkish",
    "zh": "Chinese",
}


class FallbackDict(dict):
    def __init__(self, data: dict, fallback: dict):
        super().__init__(data or {})
        self._fallback = fallback or {}

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        if key in self._fallback:
            return self._fallback[key]
        return key

    def get(self, key, default=None):
        if key in self:
            return super().get(key, default)
        return self._fallback.get(key, default)


class Language:
    """
    Language class for managing multilingual support using JSON language files.
    """

    def __init__(self):
        self.lang_codes = lang_codes
        self.lang_dir = Path("anony/locales")
        self.languages = self.load_files()

    def load_files(self):
        raw = {}
        lang_files = {file.stem: file for file in self.lang_dir.glob("*.json")}
        for lang_code, lang_file in lang_files.items():
            with open(lang_file, "r", encoding="utf-8") as file:
                raw[lang_code] = json.load(file)
        fallback = raw.get("en", {})
        languages = {code: FallbackDict(data, fallback) for code, data in raw.items()}
        logger.info(f"Loaded languages: {', '.join(languages.keys())}")
        return languages

    async def get_lang(self, chat_id: int) -> dict:
        lang_code = await db.get_lang(chat_id)
        return self.languages[lang_code]

    def get_languages(self) -> dict:
        files = {f.stem for f in self.lang_dir.glob("*.json")}
        return {code: self.lang_codes[code] for code in sorted(files)}

    def language(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                fallen = next(
                    (
                        arg
                        for arg in args
                        if hasattr(arg, "chat") or hasattr(arg, "message")
                    ),
                    None,
                )

                if not fallen.from_user:
                    return

                if hasattr(fallen, "chat"):
                    chat = fallen.chat
                elif hasattr(fallen, "message"):
                    chat = fallen.message.chat

                if chat.id in db.blacklisted:
                    logger.warning(f"Chat {chat.id} is blacklisted, leaving...")
                    return await chat.leave()

                lang_code = await db.get_lang(chat.id)
                lang_dict = self.languages[lang_code]

                setattr(fallen, "lang", lang_dict)
                try:
                    return await func(*args, **kwargs)
                except (errors.Forbidden, errors.exceptions.Forbidden):
                    logger.warning(f"Cannot write to chat {chat.id}, leaving...")
                    return await chat.leave()

            return wrapper

        return decorator
