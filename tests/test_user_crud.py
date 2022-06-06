from tests.utils.db import AsyncTestSession
from tests.utils.user import add_test_user, generate_test_user_data, get_user_by_filters
from tests.utils.dependencies import get_async_session_test, authenticated_user
from colmasys import app, get_async_session
from colmasys.models import User
from sqlalchemy import select 
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class StudentTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, 'admin')
    async def test_post_student(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = generate_test_user_data(username='new_student')
            response = await async_client.post('/student', json=data)
        self.assertEqual(response.status_code, 201)

        user = await get_user_by_filters(username='new_student')
        self.assertIsNotNone(user)

    @authenticated_user(app, 'admin')
    async def test_get_professor_exists_by_id(self):
        user = await get_user_by_filters(username='professor')
        professor_id = user.id

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/professor/id/{professor_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), 'professor')
    
    @authenticated_user(app, 'admin')
    async def test_get_student_exists_by_username(self):
        user = await get_user_by_filters(username='student')
        student_username = user.username

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/student/username/{student_username}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), 'student')

    @authenticated_user(app, 'admin')
    async def test_get_professor_not_exists(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/professor/id/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'User Not Found'})

    @authenticated_user(app, 'admin')
    async def test_get_students(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/students')
        self.assertEqual(response.status_code, 200)

    @authenticated_user(app, 'admin')
    async def test_put_professor(self):
        await add_test_user(username='edited_professor')
        professor = await get_user_by_filters(username='edited_professor')
        self.assertEqual(professor.firstname, 'edited_professor')

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = generate_test_user_data(username='edited_professor')
            data['firstname'] = 'edited_firstname'
            response = await async_client.put(f'/professor/{professor.id}', json=data)
        self.assertEqual(response.status_code, 200)
        edited_professor = await get_user_by_filters(username='edited_professor')
        self.assertEqual(edited_professor.firstname, 'edited_firstname')

    @authenticated_user(app, 'admin')
    async def test_delete_student(self):
        await add_test_user(username='deleted_student')
        student = await get_user_by_filters(username='deleted_student')
        self.assertFalse(student.deleted)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/student/{student.id}')
        self.assertEqual(response.status_code, 200)
        deleted_student = await get_user_by_filters(username='deleted_student')
        self.assertTrue(deleted_student.deleted)
