from tests.utils.db import AsyncTestSession
from colmasys.models import Vote, PostVote, CommentVote
from sqlalchemy import select

async def add_test_vote(account, post=None, comment=None, **kwargs):
    async with AsyncTestSession() as session, session.begin():
        if post:
            vote = PostVote(**kwargs)
            vote.post = post
        elif comment:
            vote = CommentVote(**kwargs)
            vote.comment = comment
        
        vote.account = account
        session.add(vote)
        await session.commit()
    return vote

#async def get_post_by_filters(**kwargs) -> Vote:
#    async with AsyncTestSession() as session, session.begin():
#        query = select(Post).filter_by(**kwargs)
#        result = await session.execute(query)
#        post = result.scalars().first()
#    return post
