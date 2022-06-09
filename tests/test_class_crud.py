from tests.utils.db import AsyncTestSession
from tests.utils.class_ import get_class_by_filters, add_test_class
from tests.utils.dependencies import get_async_session_test, authenticated_user
from colmasys import app, get_async_session
from sqlalchemy import select 
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class ClassTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, 'admin')
    async def test_post_class(self):
        data = {'academic_year': '2022/2023', 'year': 3, 'group': 2, 'major': 'IIR'}
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.post('/class', json=data)
        self.assertEqual(response.status_code, 201)

        class_ = await get_class_by_filters(**data)
        self.assertIsNotNone(class_)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.post('/class', json=data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {'detail': 'Class Already Exists'})

    @authenticated_user(app, 'admin')
    async def test_get_class_exists(self):
        data = {'academic_year': '2021/2022', 'year': 3, 'group': 2, 'major': 'IIR'}
        class_ = await get_class_by_filters(**data)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/class/{class_.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('major'), 'IIR')
  
    @authenticated_user(app, 'admin')
    async def test_get_class_not_exists(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/class/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Class Not Found'})

    @authenticated_user(app, 'admin')
    async def test_get_classes(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/classes')
        self.assertEqual(response.status_code, 200)

    @authenticated_user(app, 'admin')
    async def test_put_class(self):
        class_ = await add_test_class(academic_year='2019/2020', year=3, group=2, major='IIR')
        self.assertEqual(class_.major, 'IIR')

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'academic_year': '2019/2020', 'year': 3, 'group': 2, 'major': 'GC'}
            response = await async_client.put(f'/class/{class_.id}', json=data)
        self.assertEqual(response.status_code, 200)
        edited_class = await get_class_by_filters(id=class_.id)
        self.assertEqual(edited_class.major, 'GC')
    
    @authenticated_user(app, 'admin')
    async def test_delete_student(self):
        class_ = await add_test_class(academic_year='2019/2020', year=3, group=2, major='IIR')
        self.assertFalse(class_.deleted)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/class/{class_.id}')
        self.assertEqual(response.status_code, 200)
        deleted_class = await get_class_by_filters(id=class_.id)
        self.assertTrue(deleted_class.deleted)
