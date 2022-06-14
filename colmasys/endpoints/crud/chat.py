from colmasys import app, get_async_session
from colmasys.core import auth_required
from colmasys.models import Chat
from colmasys.utils.account import get_account_by
from fastapi import Depends
from sqlalchemy import select

@app.get('/chats')
async def get_chats(async_session=Depends(get_async_session), authenticated_user_id=Depends(auth_required.auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=authenticated_user_id)
    return [chat.serialize() for chat in account.chats]
