import os
from typing import Dict, List, Optional

import httpx
from dotenv import load_dotenv
from logger_config import setup_logger

load_dotenv()
logger = setup_logger(__name__)

base_post_api = os.getenv("API_URL", "http://fastapi:8000/api/") + "posts"


async def request_posts_data() -> Optional[List[Dict]]:
    """
    Асинхронно выполняет GET-запрос к API для получения списка всех постов.
    :return: Список словарей с данными постов или None при ошибке.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_post_api)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Ошибка при получении постов: %s", e, exc_info=True)
            return None


async def request_post_detail_data(post_id: int | str) -> Optional[Dict]:
    """
    Асинхронно выполняет GET-запрос к API для получения детальной информации о посте.

    :param post_id: ID поста для запроса
    :return: Словарь с данными поста или None при ошибке.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_post_api}/{post_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("Пост с id %s не найден", post_id)
                return {}
            logger.error(
                "HTTP ошибка при получении поста %s: %s", post_id, e, exc_info=True
            )
            return None
        except Exception as e:
            logger.error(
                "Ошибка при получении детальной информации о посте с id %s : %s",
                post_id,
                e,
                exc_info=True,
            )
            return None
