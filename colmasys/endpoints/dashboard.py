from colmasys import app, get_async_session
from colmasys.models import Model, Professor, Student, Class
from colmasys.core import auth_required
from colmasys.utils.dashboard import number_of_rows, get_majors_students_chart, get_attendance_chart
from fastapi import Depends, HTTPException

@app.get('/dashboard')
async def get_dashboard(async_session=Depends(get_async_session), _=Depends(auth_required.admin_auth_required)):
    async with async_session() as session, session.begin():
        majors_students_chart = await get_majors_students_chart(session)
        attendance_chart = await get_attendance_chart(session)

    async with async_session() as session, session.begin():
        return {
            'professors': await number_of_rows(session, Professor),
            'students': await number_of_rows(session, Student),
            'classes': await number_of_rows(session, Class),
            'majors_students_chart': majors_students_chart,
            'attendance_chart': attendance_chart
        }
