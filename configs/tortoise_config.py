import os

from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB")

TORTOISE_ORM = {
    "connections": {
        # Dict format for connection
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "database": database,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
