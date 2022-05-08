from colmasys import app, auth, get_async_session
from colmasys.core.auth import AuthCreds
from colmasys.models import User, UserModel
from fastapi import HTTPException, Depends
from sqlalchemy import select

@app.post('/login')
async def login(auth_creds: AuthCreds, async_session=Depends(get_async_session)):
    username, password = auth_creds.data
    async with async_session() as session, session.begin():
        query = select(User).filter_by(username=username)
        result = await session.execute(query)
        user = result.scalars().first()
        if user and auth.check_password(password, user.password):
            return {'token': auth.encode_token(user.id, user.user_type)}

    raise HTTPException(status_code=401, detail = 'Invalid Username/Password')
