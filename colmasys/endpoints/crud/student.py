from colmasys import app, get_async_session
from colmasys.models import User, UserModel
from colmasys.core import auth_required
from fastapi import Depends, HTTPException
from sqlalchemy import select

@app.post('/student', status_code=201)
async def post_student(user_model: UserModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        user = User.from_model(user_model)
        session.add(user)
        await session.commit()

@app.get('/student/{user_id}')
async def get_student(user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalars().first()
    
    if user:
        return user.serialize()
    else:
        raise HTTPException(status_code=404, detail='User Not Found')

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
