from colmasys import app, get_async_session
from colmasys.models import PostVote, CommentVote, VoteModel, Post, Comment
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/post/{post_id}/vote', status_code=201)
@app.post('/comment/{comment_id}/vote', status_code=201)
async def post_vote(
  request: Request, vote_model: VoteModel, post_id: int=None, comment_id: int=None,
  async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)
):
    path_type = request.url._url.split('/')[-3]

    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        
        if path_type == 'post':
            last_vote = (await session.execute(
                select(PostVote)
                .filter_by(post_id=post_id, account_id=authenticated_user_id, deleted=False)
                .order_by(PostVote.id.desc())
            )).scalars().first()

            if last_vote:
                if last_vote.value == vote_model.value:
                    last_vote.deleted = True
                    data = {'type': None}
                else:
                    last_vote.value = vote_model.value
                    data = {'type': 'upvote' if vote_model.value else 'downvote'}
            else:
                query = select(Post).filter_by(id=post_id)
                post = (await session.execute(query)).scalars().first()
                vote = PostVote.from_model(vote_model)
                vote.post = post
                vote.account = account
                session.add(vote)
                data = {'type': 'upvote' if vote_model.value else 'downvote'}

            query = select(Post).filter_by(id=post_id)
            post = (await session.execute(query)).scalars().first()
            n_votes = post.n_votes
        
        elif path_type == 'comment':
            last_vote = (await session.execute(
                select(CommentVote)
                .filter_by(comment_id=comment_id, account_id=authenticated_user_id, deleted=False)
                .order_by(CommentVote.id.desc())
            )).scalars().first()

            if last_vote:
                if last_vote.value == vote_model.value:
                    last_vote.deleted = True
                    data = {'type': None}
                else:
                    last_vote.value = vote_model.value
                    data = {'type': 'upvote' if vote_model.value else 'downvote'}
            else:
                query = select(Comment).filter_by(id=comment_id)
                comment = (await session.execute(query)).scalars().first()
                vote = CommentVote.from_model(vote_model)
                vote.comment = comment
                vote.account = account
                session.add(vote)
                data = {'type': 'upvote' if vote_model.value else 'downvote'}
            
            query = select(Comment).filter_by(id=comment_id)
            comment = (await session.execute(query)).scalars().first()
            n_votes = comment.n_votes

        await session.commit()

        data.update({'n_votes': n_votes})
        return data

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
