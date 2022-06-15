from colmasys import app, get_async_session
from colmasys.models import Model, Professor, Student, Class
from colmasys.core import auth_required
from colmasys.utils.dashboard import number_of_rows
from fastapi import Depends, HTTPException
from sqlalchemy import func, select


@app.get('/dashboard')
async def get_dashboard(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        return {
            'professors': await number_of_rows(session, Professor),
            'students': await number_of_rows(session, Student),
            'classes': await number_of_rows(session, Class)
        }
