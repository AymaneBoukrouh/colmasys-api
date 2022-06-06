from colmasys.models import Class
from sqlalchemy import select

async def class_filter_by_scalars(session, **kwargs):
    query = select(Class).filter_by(**kwargs)
    result = await session.execute(query)
    return result.scalars()

async def get_class_by(session, **kwargs):
    scalars = await class_filter_by_scalars(session, **kwargs)
    return scalars.first()
