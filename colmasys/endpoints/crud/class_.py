from colmasys import app, get_async_session
from colmasys.models import Class, ClassModel
from colmasys.core import auth_required
from colmasys.utils.class_ import get_class_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/class', status_code=201)
async def post_class(request: Request, class_model: ClassModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(Class).filter_by(**class_model.dict())
        result = await session.execute(query)
        class_ = result.scalars().first()
        if class_:
            raise HTTPException(status_code=409, detail='Class Already Exists')

        class_ = Class.from_model(class_model)
        session.add(class_)
        await session.commit()

@app.get('/classes')
async def get_classes(request: Request, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(Class)
        result = await session.execute(query)
        classes = result.scalars().all()
    return [class_.serialize() for class_ in classes]

@app.get('/class/{class_id}')
async def get_class_by_id(class_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (class_ := await get_class_by(session, id=class_id)):
            return class_.serialize()
        else:
            raise HTTPException(status_code=404, detail='Class Not Found')

@app.put('/class/{class_id}')
async def put_class(class_model: ClassModel, class_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        class_ = await get_class_by(session, id=class_id)
        class_.update_from_model(class_model)
        await session.commit()

@app.delete('/class/{class_id}')
async def delete_class(class_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (class_ := await get_class_by(session, id=class_id)):
            class_.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Class Not Found')
