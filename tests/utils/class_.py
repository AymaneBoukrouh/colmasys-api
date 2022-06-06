from tests.utils.db import AsyncTestSession
from colmasys.models import Class
from sqlalchemy import select

async def add_test_class(**kwargs):
    async with AsyncTestSession() as session, session.begin():
        class_ = Class(**kwargs)
        session.add(class_)
        await session.commit()
    return class_

async def get_class_by_filters(**kwargs) -> Class:
    async with AsyncTestSession() as session, session.begin():
        query = select(Class).filter_by(**kwargs)
        result = await session.execute(query)
        class_ = result.scalars().first()
    return class_
