from colmasys import app, get_async_session
from colmasys.models import Account, AccountModel
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by, register_account_by_type, get_accounts_by_type
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/professor', status_code=201)
@app.post('/student', status_code=201)
async def post_account(request: Request, account_model: AccountModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    path_end = request.url._url.split('/')[-1]
    async with async_session() as session, session.begin():
        account_type = Account.Type.Professor if (path_end == 'professor') else Account.Type.Student
        await register_account_by_type(session, account_model, account_type)

@app.get('/professors')
@app.get('/students')
async def get_accounts(request: Request, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    path_end = request.url._url.split('/')[-1]
    async with async_session() as session, session.begin():
        account_type = Account.Type.Professor if (path_end == 'professors') else Account.Type.Student
        return await get_accounts_by_type(session, account_type)

@app.get('/professor/id/{account_id}')
@app.get('/student/id/{account_id}')
async def get_account_by_id(account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, id=account_id)):
            return account.serialize()
        else:
            raise HTTPException(status_code=404, detail='Account Not Found')

@app.get('/professor/username/{username}')
@app.get('/student/username/{username}')
async def get_user_by_username(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, username=username)):
            return account.serialize()
        else:
            raise HTTPException(status_code=404, detail='Account Not Found')

@app.put('/professor/{account_id}')
@app.put('/student/{account_id}')
async def put_account(account_model: AccountModel, account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=account_id)
        account.update_from_model(account_model)
        await session.commit()

@app.delete('/professor/{account_id}')
@app.delete('/student/{account_id}')
async def deleted_account(account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, id=account_id)):
            account.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Account Not Found')
