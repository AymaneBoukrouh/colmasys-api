from tests.utils.db import AsyncTestSession
from tests.utils.class_ import get_class_by_filters, add_test_class
from tests.utils.user import get_user_by_filters, add_test_user
from tests.utils.dependencies import get_async_session_test, authenticated_user
from colmasys import app, get_async_session
from colmasys.models import User
from sqlalchemy import select 
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class ClassStudentTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, 'admin')
    async def test_add_student_to_class(self):
        new_student = await add_test_user(username='new_iir_student', user_type=User.Type.student)
        new_class = await add_test_class(academic_year='2019/2020', year=1, group=1, major='IIR')
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.post(f'/class/{new_class.id}/student/{new_student.id}')
        self.assertEqual(response.status_code, 200)

        student = await get_user_by_filters(id=new_student.id)
        self.assertEqual(student.class_id, new_class.id)

    @authenticated_user(app, 'admin')
    async def test_remove_student_from_class(self):
        new_student = await add_test_user(username='new_20182019_3irr_g2_student', user_type=User.Type.student)
        new_class = await add_test_class(academic_year='2018/2019', year=3, group=2, major='IIR')
        async with AsyncTestSession() as session, session.begin():
            query = select(User).filter_by(id=new_student.id)
            result = await session.execute(query)
            student = result.scalars().first()
            student.class_id = new_class.id
            await session.commit()

        student = await get_user_by_filters(id=new_student.id)
        self.assertEqual(student.class_id, new_class.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/class/{new_class.id}/student/{new_student.id}')
        self.assertEqual(response.status_code, 200)

        student = await get_user_by_filters(id=new_student.id)
        self.assertIsNone(student.class_id)

    @authenticated_user(app, 'admin')
    async def test_get_students_of_class(self):
        new_class = await add_test_class(academic_year='2018/2019', year=1, group=1, major='GC')
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/class/{new_class.id}/students')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

        new_student = await add_test_user(username='new_20182019_1gc_g1_student')
        async with AsyncTestSession() as session, session.begin():
            query = select(User).filter_by(id=new_student.id)
            result = await session.execute(query)
            student = result.scalars().first()
            student.class_id = new_class.id
            await session.commit()
        
        student = await get_user_by_filters(id=new_student.id)
        self.assertEqual(student.class_id, new_class.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/class/{new_class.id}/students')
        
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0], student.serialize())
