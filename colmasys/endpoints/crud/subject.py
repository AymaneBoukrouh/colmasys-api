from colmasys import app, get_async_session
from colmasys.models import Subject, SubjectModel
from colmasys.core import auth_required
from colmasys.utils.subject import get_subject_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/subject', status_code=201)
async def post_subject(subject_model: SubjectModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(Subject).filter_by(name=subject_model.name)
        result = await session.execute(query)
        subject = result.scalars().first()
        if subject:
            raise HTTPException(status_code=409, detail='Subject Already Exists')

        subject = Subject.from_model(subject_model)
        session.add(subject)
        await session.commit()

@app.get('/subjects')
async def get_subjectes(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(Subject)
        result = await session.execute(query)
        subjects = result.scalars().all()
    return [subject.serialize() for subject in subjects]

@app.get('/subject/{subject_id}')
async def get_subjectby_id(subject_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (subject := await get_subject_by(session, id=subject_id)):
            return subject.serialize()
        else:
            raise HTTPException(status_code=404, detail='Subject Not Found')

@app.put('/subject/{subject_id}')
async def put_subject(subject_model: SubjectModel, subject_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        subject = await get_subject_by(session, id=subject_id)
        subject.update_from_model(subject_model)
        await session.commit()

@app.delete('/subject/{subject_id}')
async def delete_subject(subject_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (subject := await get_subject_by(session, id=subject_id)):
            subject.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Subject Not Found')
