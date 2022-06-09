from colmasys.models import Student
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid

async def student_filter_by_scalars(session, **kwargs):
    query = select(Student).filter_by(**kwargs)
    result = await session.execute(query)
    return result.scalars()

async def get_student_by(session, **kwargs):
    scalars = await student_filter_by_scalars(session, **kwargs)
    return scalars.first()
