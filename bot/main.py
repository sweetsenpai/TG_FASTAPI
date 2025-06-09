#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import re

import httpx
from dotenv import load_dotenv
from logger_config import setup_logger
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

load_dotenv()
token = os.getenv("BOT_TOKEN")


logging.getLogger("httpx").setLevel(logging.WARNING)

logger = setup_logger(__name__)
logger.info("Стартуем бота")


def escape_markdown_v2(text: str) -> str:
    # Экранируем все специальные символы MarkdownV2 согласно документации
    return re.sub(r"([_*[\]()~`>#+\-=|{}.!\\])", r"\\\1", text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def get_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://fastapi:8000/api/posts")
            posts = response.json()
        except Exception as e:
            logger.error("Ошибка при получении постов: %s", e, exc_info=True)
            await update.message.reply_text(
                "Сервис времено не доступен, попробуйте позже."
            )
    if not posts:
        await update.message.reply_text("Постов пока нет.")
        return

    keyboard_buttons = [
        [
            InlineKeyboardButton(
                text=f"{post['title']}",
                callback_data="post_id:" + str(post["id"]),
            )
        ]
        for post in posts
    ]

    await update.message.reply_text(
        text="Доступные посты", reply_markup=InlineKeyboardMarkup(keyboard_buttons)
    )


async def detail_post_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    post_id = int(query.data.replace("post_id:", ""))
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://fastapi:8000/api/posts/{post_id}")
            post_data = response.json()
        except Exception as e:
            logger.error("Ошибка при получении постов: %s", e, exc_info=True)

    if not post_data:
        await query.answer(show_alert=True, text="Данный пост больше не существует")
    await query.answer()

    text = f"*{post_data['title']}*\nДата создания: _{escape_markdown_v2(post_data['date_of_creation'][:10])}_\n\n{post_data['text']}"
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Назад", callback_data="posts_menu")]]
        ),
        parse_mode="MarkdownV2",
    )


async def back_to_post_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://fastapi:8000/api/posts")
            posts = response.json()
        except Exception as e:
            logger.error("Ошибка при получении постов: %s", e, exc_info=True)
            await update.message.reply_text(
                "Сервис времено не доступен, попробуйте позже."
            )

    if not posts:
        await query.edit_message_text("Постов пока нет.")

    keyboard_buttons = [
        [
            InlineKeyboardButton(
                text=post["title"],
                callback_data="post_id:" + str(post["id"]),
            )
        ]
        for post in posts
    ]

    await query.edit_message_text(
        text="Доступные посты", reply_markup=InlineKeyboardMarkup(keyboard_buttons)
    )


def main() -> None:

    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("posts", get_posts))
    application.add_handler(
        CallbackQueryHandler(detail_post_info, pattern=r"^post_id:\d+$")
    )
    application.add_handler(
        CallbackQueryHandler(back_to_post_menu, pattern=r"^posts_menu")
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
