from api_client import request_post_detail_data, request_posts_data
from keyboards import generate_posts_keyboard
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import generate_post_message_text

SERVICE_UNAVAILABLE_TEXT = "Сервис временно не доступен, попробуйте позже."

NO_POSTS_TEXT = "Постов пока нет."

POST_NOT_FOUND_TEXT = "Данный пост больше не существует."


async def get_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает команду /posts и возвращает сообщение с InlineKeyboardMarkup для получения детальной информации по посту.
    :param update: Update
    :param context:  ContextTypes.DEFAULT_TYPE
    :return: Сообщение с детальной информацией по посту или сообщение об ошибке.
    """
    posts = await request_posts_data()

    if posts is None:
        await update.message.reply_text(SERVICE_UNAVAILABLE_TEXT)
        return

    if not posts:
        await update.message.reply_text(NO_POSTS_TEXT)
        return

    keyboard_posts = generate_posts_keyboard(posts)

    await update.message.reply_text(text="Доступные посты", reply_markup=keyboard_posts)


async def detail_post_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает callback кнопок меню постов и возвращает текст и дату создания поста.
    :param update:
    :param context:
    :return: Детальная информация о посте или сообщение
    """
    query = update.callback_query
    post_id = query.data.replace("post_id:", "")
    post_data = await request_post_detail_data(post_id)

    if post_data is None:
        await query.answer(show_alert=True, text=SERVICE_UNAVAILABLE_TEXT)
        return

    if not post_data:
        await query.answer(show_alert=True, text=POST_NOT_FOUND_TEXT)
        posts = await request_posts_data()
        updated_keyboard = generate_posts_keyboard(posts)
        await query.edit_message_reply_markup(updated_keyboard)
        return

    msg_text = generate_post_message_text(post_data)
    await query.edit_message_text(
        text=msg_text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Назад", callback_data="posts_menu")]]
        ),
        parse_mode="MarkdownV2",
    )


async def back_to_post_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает callback кнопки "назад" под полным текстом поста
    :param update:
    :param context:
    :return: Возвращает меню поста или сообщает об ошибке/отсутствии постов
    """
    query = update.callback_query
    posts = await request_posts_data()

    if not posts:
        await query.edit_message_text(NO_POSTS_TEXT)
    if posts is None:
        await query.answer(show_alert=True, text=NO_POSTS_TEXT)

    keyboard_buttons = generate_posts_keyboard(posts)
    await query.edit_message_text(text="Доступные посты", reply_markup=keyboard_buttons)
