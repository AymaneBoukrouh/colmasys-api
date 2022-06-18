from colmasys import app, get_async_session
from colmasys.models import Account, AccountModel, professor, Professor
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by, register_professor, get_professors
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/professor', status_code=201)
async def post_professor(account_model: AccountModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        await register_professor(session, account_model)

@app.get('/professors')
async def get_professors_(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        return await get_professors(session)

@app.get('/professor/id/{account_id}')
async def get_professor_by_id(account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, id=account_id)):
            return account.serialize()
        else:
            raise HTTPException(status_code=404, detail='Professor Not Found')

@app.get('/professor/username/{username}')
async def get_user_by_username(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, username=username)):
            return account.serialize()
        else:
            raise HTTPException(status_code=404, detail='Professor Not Found')

@app.put('/professor/{account_id}')
async def put_professor(account_model: AccountModel, account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=account_id)
        account.update_from_model(account_model)
        await session.commit()

@app.delete('/professor/{account_id}')
async def deleted_professor(account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, id=account_id)):
            account.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Professor Not Found')
