from colmasys import app, get_async_session
from colmasys.models import PostVote, CommentVote, VoteModel, Post, Comment
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/post/{post_id}/vote', status_code=201)
@app.post('/comment/{comment_id}/vote', status_code=201)
async def post_account(
  request: Request, vote_model: VoteModel, post_id: int=None, comment_id: int=None,
  async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)
):
    path_type = request.url._url.split('/')[-3]

    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        
        if path_type == 'post':
            query = select(Post).filter_by(id=post_id)
            post = (await session.execute(query)).scalars().first()

            vote = PostVote.from_model(vote_model)
            vote.post = post

        elif path_type == 'comment':
            query = select(Comment).filter_by(id=comment_id)
            comment = (await session.execute(query)).scalars().first()
            
            vote = CommentVote.from_model(vote_model)
            vote.comment = comment
        
        vote.account = account
        session.add(vote)
        await session.commit()

@app.get('/post/{post_id}/votes')
@app.get('/comment/{comment_id}/votes')
async def get_votes(
  request: Request, post_id: int=None, comment_id: int=None,
  async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)
):
    path_type = request.url._url.split('/')[-3]
    async with async_session() as session, session.begin():
        if path_type == 'post':
            votes = (await session.execute(select(Post).filter_by(id=post_id))).scalars().first().votes
        elif path_type == 'comment':
            votes = (await session.execute(select(Comment).filter_by(id=comment_id))).scalars().first().votes

        return [vote.serialize() for vote in votes]
