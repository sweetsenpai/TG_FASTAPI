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
logger.info("Бот запустился и начал работу")


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
