from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "posts" ADD "text" TEXT NOT NULL;
        ALTER TABLE "posts" DROP COLUMN "test";
        ALTER TABLE "posts" ALTER COLUMN "title" TYPE VARCHAR(256) USING "title"::VARCHAR(256);
        COMMENT ON COLUMN "posts"."title" IS 'Название поста';
        ALTER TABLE "posts" ALTER COLUMN "date_of_creation" TYPE TIMESTAMPTZ USING "date_of_creation"::TIMESTAMPTZ;
        COMMENT ON COLUMN "posts"."date_of_creation" IS 'Дата создания поста';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "posts" ADD "test" TEXT NOT NULL;
        ALTER TABLE "posts" DROP COLUMN "text";
        COMMENT ON COLUMN "posts"."title" IS NULL;
        ALTER TABLE "posts" ALTER COLUMN "title" TYPE VARCHAR(256) USING "title"::VARCHAR(256);
        COMMENT ON COLUMN "posts"."date_of_creation" IS NULL;
        ALTER TABLE "posts" ALTER COLUMN "date_of_creation" TYPE TIMESTAMPTZ USING "date_of_creation"::TIMESTAMPTZ;"""
