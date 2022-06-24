from colmasys import app, auth, get_async_session
from colmasys.core.auth import AuthCreds
from colmasys.models import Account, AccountModel
from fastapi import HTTPException, Depends
from sqlalchemy import select

@app.post('/login')
async def login(auth_creds: AuthCreds, async_session=Depends(get_async_session)):
    username, password = auth_creds.data
    async with async_session() as session, session.begin():
        query = select(Account).filter_by(username=username)
        result = await session.execute(query)
        account = result.scalars().first()
        #if account and auth.check_password(password, account.password):
        #    return {'token': auth.encode_token(account.id, account.account_type)}
        if account:
            return {'token': auth.encode_token(account.id, account.account_type)}

    raise HTTPException(status_code=401, detail = 'Invalid Username/Password')
