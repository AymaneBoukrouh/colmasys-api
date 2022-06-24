from colmasys import app, get_async_session
from colmasys.models import Post, PostModel
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.get('/feed')
async def get_posts(async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
        return [post.serialize() for post in account.posts]
