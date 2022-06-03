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
    async def test_get_student_exists(self):
        user = await get_user_by_filters(username='student')
        student_id = user.id

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'id': student_id}
            response = await async_client.request('GET', '/student', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), 'student')

    @authenticated_user(app, 'admin')
    async def test_get_student_not_exists(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'id': 100}
            response = await async_client.request('GET', '/student', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'User Not Found'})
    
    @authenticated_user(app, 'admin')
    async def test_get_student_arguments_required(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = dict()
            response = await async_client.request('GET', '/student', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Arguments Required'})

    @authenticated_user(app, 'admin')
    async def test_get_student_too_many_arguments(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'id': 1, 'username': 'student'}
            response = await async_client.request('GET', '/student', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'detail': 'Too Many Arguments'})

    @authenticated_user(app, 'admin')
    async def test_get_students(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/students')
        self.assertEqual(response.status_code, 200)

    @authenticated_user(app, 'admin')
    async def test_put_student(self):
        await add_test_user(username='edited_student')
        student = await get_user_by_filters(username='edited_student')
        self.assertEqual(student.firstname, 'edited_student')

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = generate_test_user_data(username='edited_student')
            data['firstname'] = 'edited_firstname'
            response = await async_client.put(f'/student/{student.id}', json=data)
        self.assertEqual(response.status_code, 200)
        edited_student = await get_user_by_filters(username='edited_student')
        self.assertEqual(edited_student.firstname, 'edited_firstname')

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
