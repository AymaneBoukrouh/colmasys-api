from colmasys.models import User
from sqlalchemy import select

async def get_user_by(session, **kwargs):
    query = select(User).filter_by(**kwargs)
    result = await session.execute(query)
    user = result.scalars().first()
    return user
