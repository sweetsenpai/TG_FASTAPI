import re
from typing import Dict


def format_to_markdown(text: str) -> str:
    """
    Экранирует все специальные символы Markdovn
    :param text: входной текст
    :return:  выходной текст пригодный для форматирования Markdown
    """
    return re.sub(r"([_*[\]()~`>#+\-=|{}.!\\])", r"\\\1", text)


def generate_post_message_text(post_data: Dict) -> str:
    """
    Получает словарь поста и обрабатывает поля для экранирования символов Markdown
    :param post_data: Данные поста
    :return: Обработанные текст
    """
    text = (
        f"*{format_to_markdown(post_data['title'])}*\n"
        f"Дата создания: _{format_to_markdown(post_data['date_of_creation'])}_\n\n"
        f"{format_to_markdown(post_data['text'])}"
    )
    return text
