from colmasys import app, get_async_session
from colmasys.models import Account, AccountModel, StudentModel, Student, Professor
from colmasys.core import auth_required
from colmasys.utils.account import get_account_by, register_student, get_students
from colmasys.utils.student import get_student_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/student', status_code=201)
async def post_student(student_model: StudentModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        await register_student(session, student_model)

@app.get('/students')
async def get_students_(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        return await get_students(session)

@app.get('/student/id/{account_id}')
async def get_student_by_id(account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, id=account_id)):
            return account.serialize()
        else:
            raise HTTPException(status_code=404, detail='Student Not Found')

@app.get('/student/username/{username}')
async def get_user_by_username(username: str, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, username=username)):
            student = await get_student_by(session, id=account.user.id)
            return student.serialize()
        else:
            raise HTTPException(status_code=404, detail='Student Not Found')

@app.put('/student/{account_id}')
async def put_student(student_model: StudentModel, account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    student_dict = student_model.dict()
    class_id = student_dict.pop('class_id', None)
    account_model = AccountModel(**student_dict)
    
    async with async_session() as session, session.begin():
        account = await get_account_by(session, id=account_id)
        account.update_from_model(account_model)
        account.user.class_id = class_id
        await session.commit()

@app.delete('/student/{account_id}')
async def deleted_student(account_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (account := await get_account_by(session, id=account_id)):
            account.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Student Not Found')
