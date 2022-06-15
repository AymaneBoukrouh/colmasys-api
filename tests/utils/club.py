from tests.utils.db import AsyncTestSession
from colmasys.models import Club
from sqlalchemy import select

async def add_test_club(**kwargs):
    async with AsyncTestSession() as session, session.begin():
        club = Club(**kwargs)
        session.add(club)
        await session.commit()
    return club

async def get_club_by_filters(**kwargs) -> Club:
    async with AsyncTestSession() as session, session.begin():
        query = select(Club).filter_by(**kwargs)
        result = await session.execute(query)
        club = result.scalars().first()
    return club
