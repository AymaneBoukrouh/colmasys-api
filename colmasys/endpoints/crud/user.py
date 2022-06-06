from colmasys import app, get_async_session
from colmasys.models import User, UserModel
from colmasys.core import auth_required
from colmasys.utils.user import get_user_by, register_user_by_type, get_users_by_type
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/professor', status_code=201)
@app.post('/student', status_code=201)
async def post_user(request: Request, user_model: UserModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    path_end = request.url._url.split('/')[-1]
    async with async_session() as session, session.begin():
        user_type = User.Type.professor if (path_end == 'professor') else User.Type.student
        await register_user_by_type(session, user_model, user_type)

@app.get('/professors')
@app.get('/students')
async def get_users(request: Request, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    path_end = request.url._url.split('/')[-1]
    async with async_session() as session, session.begin():
        user_type = User.Type.professor if (path_end == 'professors') else User.Type.student
        return await get_users_by_type(session, user_type)

@app.get('/professor/id/{user_id}')
@app.get('/student/id/{user_id}')
async def get_user_by_id(user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (user := await get_user_by(session, id=user_id)):
            return user.serialize()
        else:
            raise HTTPException(status_code=404, detail='User Not Found')

@app.get('/professor/username/{username}')
@app.get('/student/username/{username}')
async def get_user_by_username(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (user := await get_user_by(session, username=username)):
            return user.serialize()
        else:
            raise HTTPException(status_code=404, detail='User Not Found')

@app.put('/professor/{user_id}')
@app.put('/student/{user_id}')
async def put_user(user_model: UserModel, user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        user = await get_user_by(session, id=user_id)
        user.update_from_model(user_model)
        await session.commit()

@app.delete('/professor/{user_id}')
@app.delete('/student/{user_id}')
async def deleted_user(user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (user := await get_user_by(session, id=user_id)):
            user.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='User Not Found')
