from colmasys import app, get_async_session
from colmasys.models import Post, PostModel
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/post', status_code=201)
async def post_post(post_model: PostModel, async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        post = Post.from_model(post_model)
        post.author = await get_account_by(session, id=authenticated_user_id)
        session.add(post)
        await session.commit()

@app.get('/user/{username}/posts')
async def get_posts(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, username=username)
        return [post.serialize() for post in account.posts]

@app.get('/post/{post_id}')
async def get_post(post_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        query = select(Post).filter_by(id=post_id)
        post = (await session.execute(query)).scalars().first()
        
        if post:
            return post.serialize()
        else:
            raise HTTPException(status_code=404, detail='Post Not Found')

@app.put('/post/{post_id}')
async def put_post(post_model: PostModel, post_id: int, async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        query = select(Post).filter_by(id=post_id)
        post = (await session.execute(query)).scalars().first()

        if post.author == account:
            post.update_from_model(post_model)
            await session.commit()
        else:
            raise HTTPException(status_code=403, detail='Forbidden')

@app.delete('/post/{post_id}')
async def delete_post(post_id: int, async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        query = select(Post).filter_by(id=post_id)
        post = (await session.execute(query)).scalars().first()

        if post:
            if post.author == account:
                post.deleted = True
                await session.commit()
            else:
                raise HTTPException(status_code=403, detail='Forbidden')
              
        else:
            raise HTTPException(status_code=404, detail='Post Not Found')
