


from colmasys import app, get_async_session
from colmasys.models import Club, ClubModel
from colmasys.core import auth_required
from colmasys.utils.club import get_club_by
from fastapi import Request, Depends, HTTPException
from sqlalchemy import select


@app.post('/club', status_code=201)
async def post_club(club_model: ClubModel, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(Club).filter_by(**club_model.dict())
        result = await session.execute(query)
        club = result.scalars().first()
        if club:
            raise HTTPException(status_code=409, detail='Club Already Exists')

        club = Club.from_model(club_model)
        session.add(club)
        await session.commit()

@app.get('/clubs')
async def get_clubs(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        query = select(Club)
        result = await session.execute(query)
        clubs = result.scalars().all()
    return [club.serialize() for club in clubs]

@app.get('/club/{club_id}')
async def get_club_by_id(club_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (club := await get_club_by(session, id=club_id)):
            return club.serialize()
        else:
            raise HTTPException(status_code=404, detail='Club Not Found')

@app.put('/club/{club_id}')
async def put_club(club_model: ClubModel, club_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        club = await get_club_by(session, id=club_id)
        club.update_from_model(club_model)
        await session.commit()

@app.delete('/club/{club_id}')
async def delete_club(club_id: int, async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        if (club := await get_club_by(session, id=club_id)):
            club.deleted = True
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Club Not Found')
