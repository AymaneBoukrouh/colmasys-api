from tests.utils.db import AsyncTestSession
from colmasys.models import Post
from sqlalchemy import select

async def add_test_post(author, **kwargs):
    async with AsyncTestSession() as session, session.begin():
        post = Post(**kwargs)
        post.author = author
        session.add(post)
        await session.commit()
    return post

async def get_post_by_filters(**kwargs) -> Post:
    async with AsyncTestSession() as session, session.begin():
        query = select(Post).filter_by(**kwargs)
        result = await session.execute(query)
        post = result.scalars().first()
    return post
