from colmasys import app, get_async_session
from colmasys.models import Comment, CommentModel, Post
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/post/{post_id}/comment', status_code=201)
async def post_comment(comment_model: CommentModel, post_id: int, async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        query = select(Post).filter_by(id=post_id)
        post = (await session.execute(query)).scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail='Post Not Found')

        comment = Comment.from_model(comment_model)
        comment.author = await get_account_by(session, id=authenticated_user_id)
        comment.post = post
        session.add(comment)
        await session.commit()

@app.get('/user/{username}/comments')
async def get_user_comments(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, username=username)
        return [comment.serialize() for comment in account.comments]

@app.get('/post/{post_id}/comments')
async def get_post_comments(post_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        query = select(Post).filter_by(id=post_id)
        post = (await session.execute(query)).scalars().first()

        return [comment.serialize() for comment in post.comments]

@app.get('/comment/{comment_id}')
async def get_comment(comment_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        query = select(Comment).filter_by(id=comment_id)
        comment = (await session.execute(query)).scalars().first()
        
        if comment:
            return comment.serialize()
        else:
            raise HTTPException(status_code=404, detail='Comment Not Found')

@app.put('/comment/{comment_id}')
async def put_comment(comment_model: CommentModel, comment_id: int, async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        query = select(Comment).filter_by(id=comment_id)
        comment = (await session.execute(query)).scalars().first()

        if comment.author == account:
            comment.update_from_model(comment_model)
            await session.commit()
        else:
            raise HTTPException(status_code=403, detail='Forbidden')

@app.delete('/comment/{comment_id}')
async def delete_comment(comment_id: int, async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        query = select(Comment).filter_by(id=comment_id)
        comment = (await session.execute(query)).scalars().first()

        if comment:
            if comment.author == account:
                comment.deleted = True
                await session.commit()
            else:
                raise HTTPException(status_code=403, detail='Forbidden')
              
        else:
            raise HTTPException(status_code=404, detail='Comment Not Found')

