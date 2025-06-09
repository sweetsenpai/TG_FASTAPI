from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(256) NOT NULL UNIQUE,
    "password" VARCHAR(256) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."email" IS 'Email пользователя';
COMMENT ON COLUMN "users"."password" IS 'Пароль пользователя';
COMMENT ON COLUMN "users"."is_active" IS 'Пользователь активен';
COMMENT ON COLUMN "users"."created_at" IS 'Дата создания акаунта';
COMMENT ON TABLE "users" IS 'Модель пользователя';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "users";"""
