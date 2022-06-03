from colmasys import app, get_async_session
from colmasys.models import User, UserModel
from colmasys.core import auth_required
from fastapi import Depends, HTTPException
from sqlalchemy import select
import uuid

@app.post('/student', status_code=201)
async def post_student(user_model: UserModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        user_model.password = str(uuid.uuid4()).split('-')[0] # random password
        user = User.from_model(user_model)
        user.user_type = User.Type.student
        session.add(user)
        await session.commit()

@app.get('/student/id/{user_id}')
async def get_student_by_id(user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalars().first()
    
    if user:
        return user.serialize()
    else:
        raise HTTPException(status_code=404, detail='User Not Found')

@app.get('/student/username/{username}')
async def get_student_by_username(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(User).filter_by(username=username)
        result = await session.execute(query)
        user = result.scalars().first()

    if user:
        return user.serialize()
    else:
        raise HTTPException(status_code=404, detail='User Not Found')

@app.get('/students')
async def get_students(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(User).filter_by(user_type=User.Type.student)
        result = await session.execute(query)
        users = result.scalars().all()
    return [user.serialize() for user in users]

@app.put('/student/{user_id}')
async def put_student(user_model: UserModel, user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        user.update_from_model(user_model)
        await session.commit()

@app.delete('/student/{user_id}')
async def deleted_student(user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalars().first()
    
        if user:
            user.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='User Not Found')
