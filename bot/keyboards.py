from typing import Dict, List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def generate_posts_keyboard(posts: List[Dict]) -> InlineKeyboardMarkup:
    """
    Генерирует InlineKeyboardMarkup на основе переданного списка постов.
    :param posts: Список постов
    :return: Клавиатуру для поста. Конпки с заголовком поста, callback - id поста.
    """
    posts_buttons = [
        [
            InlineKeyboardButton(
                text=f"{post['title']}",
                callback_data="post_id:" + str(post["id"]),
            )
        ]
        for post in posts
    ]
    return InlineKeyboardMarkup(posts_buttons)
