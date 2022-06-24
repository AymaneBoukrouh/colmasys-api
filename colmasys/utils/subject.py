from colmasys.models import Subject
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid

async def subject_filter_by_scalars(session, **kwargs):
    query = select(Subject).filter_by(**kwargs)
    result = await session.execute(query)
    return result.scalars()

async def get_subject_by(session, **kwargs):
    scalars = await subject_filter_by_scalars(session, **kwargs)
    return scalars.first()
