from tests.utils.db import AsyncTestSession
from tests.utils.user import get_account_by_filters
from tests.utils.post import get_post_by_filters
from colmasys.models import Comment
from sqlalchemy import select
import sqlalchemy

async def add_test_comment(author, post, **kwargs):
    async with AsyncTestSession() as session, session.begin():
        comment = Comment(**kwargs)
        comment.author = author
        comment.post = post
        session.add(comment)
        await session.commit()
    return comment

async def get_comment_by_filters(**kwargs) -> Comment:
    async with AsyncTestSession() as session, session.begin():
        query = select(Comment).filter_by(**kwargs)
        result = await session.execute(query)
        comment = result.scalars().first()
    return comment
