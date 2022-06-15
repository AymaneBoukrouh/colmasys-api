from colmasys.models import Club
from sqlalchemy import select

async def club_filter_by_scalars(session, **kwargs):
    query = select(Club).filter_by(**kwargs)
    result = await session.execute(query)
    return result.scalars()

async def get_club_by(session, **kwargs):
    scalars = await club_filter_by_scalars(session, **kwargs)
    return scalars.first()
