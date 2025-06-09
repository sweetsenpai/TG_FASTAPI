from app.schemas.posts import PostCreate, PostUpdate
from db.models import Posts


async def get_all_posts():
    return await Posts.all()


async def get_post(post_id: int):
    return await Posts.get_or_none(id=post_id)


async def create_post(data: PostCreate):
    return await Posts.create(**data.model_dump())


async def update_post(post, data: PostUpdate):
    post_data = data.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(post, key, value)
    await post.save()
    return post


async def delete_post(post):
    await post.delete()
