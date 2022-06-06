from colmasys import app, get_async_session
from colmasys.models import Class, ClassModel
from colmasys.core import auth_required
from colmasys.utils.class_ import get_class_by
from colmasys.utils.user import get_user_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/class/{class_id}/student/{user_id}')
async def post_class_student(class_id: int, user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        user = await get_user_by(session, id=user_id)
        user.class_id = class_id
        await session.commit()

@app.delete('/class/{class_id}/student/{user_id}')
async def delete_class_student(class_id: int, user_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        user = await get_user_by(session, id=user_id)
        user.class_id = None
        await session.commit()

@app.get('/class/{class_id}/students')
async def get_class_students(class_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        class_ = await get_class_by(session, id=class_id)
        return class_.students
