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

# import httpx
from dotenv import load_dotenv
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()
token = os.getenv("BOT_TOKEN")
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

test_response = [
    {
        "title": "string",
        "text": "string",
        "id": 4,
        "date_of_creation": "2025-06-08T15:18:00.438230Z",
    },
    {
        "title": "Юбилейный тестовый пост",
        "text": "Это юбилейный тестовый текст",
        "id": 5,
        "date_of_creation": "2025-06-08T15:55:00.979759Z",
    },
    {
        "title": "Поменяли",
        "text": "Лалалалалалалал",
        "id": 3,
        "date_of_creation": "2025-06-08T15:16:50.817298Z",
    },
    {
        "title": "string",
        "text": "",
        "id": 6,
        "date_of_creation": "2025-06-08T16:19:51.313937Z",
    },
    {
        "title": "",
        "text": "",
        "id": 7,
        "date_of_creation": "2025-06-08T16:19:57.626386Z",
    },
    {
        "title": "Мой первый пост",
        "text": "qwdfqwdqwe",
        "id": 8,
        "date_of_creation": "2025-06-08T16:37:41.762078Z",
    },
    {
        "title": "Мой не первый пост",
        "text": "Это содержимое моего не первого поста поста",
        "id": 9,
        "date_of_creation": "2025-06-09T09:25:19.725538Z",
    },
]


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def get_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # async with httpx.AsyncClient() as client:
    #     response = await client.get("http://fastapi:8000/api/posts")
    #     posts = response.json()
    posts = test_response
    if not posts:
        await update.message.reply_text("Постов пока нет.")
        return

    keyboard_buttons = [
        [
            InlineKeyboardButton(
                text=f"{post['title']} - {post['date_of_creation'][:10]}",
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
    # post_id = int(query.data.replace("post_id:", ""))
    if not test_response:
        await query.answer(show_alert=True, text="Данный пост больше не существует")
    await query.answer()
    text = f"{test_response[1]['title']}\n{test_response[1]['date_of_creation']}\n\n{test_response[1]['text']}"
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Назад", callback_data="posts_menu")]]
        ),
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("posts", get_posts))
    application.add_handler(
        CallbackQueryHandler(detail_post_info, pattern=r"^post_id:\d+$")
    )

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
