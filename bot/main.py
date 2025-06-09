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

from dotenv import load_dotenv
from logger_config import setup_logger
from posts import back_to_post_menu, detail_post_info, get_posts
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

load_dotenv()
token = os.getenv("BOT_TOKEN")


logging.getLogger("httpx").setLevel(logging.WARNING)

logger = setup_logger(__name__)
logger.info("Стартуем бота")


def main() -> None:

    application = Application.builder().token(token).build()

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
