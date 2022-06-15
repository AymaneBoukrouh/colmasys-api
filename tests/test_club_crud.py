from tests.utils.db import AsyncTestSession
from tests.utils.club import get_club_by_filters, add_test_club
from tests.utils.dependencies import get_async_session_test, authenticated_user
from colmasys import app, get_async_session
from sqlalchemy import select 
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class ClubTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, 'admin')
    async def test_post_club(self):
        data = {'name': 'Post Club'}
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.post('/club', json=data)
        self.assertEqual(response.status_code, 201)

        club = await get_club_by_filters(**data)
        self.assertIsNotNone(club)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.post('/club', json=data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {'detail': 'Club Already Exists'})

    @authenticated_user(app, 'admin')
    async def test_get_club_exists(self):
        data = {'name': 'C.S Club'}
        club = await get_club_by_filters(**data)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/club/{club.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('name'), 'C.S Club')
  
    @authenticated_user(app, 'admin')
    async def test_get_club_not_exists(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/club/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Club Not Found'})

    @authenticated_user(app, 'admin')
    async def test_get_clubs(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/clubs')
        self.assertEqual(response.status_code, 200)

    @authenticated_user(app, 'admin')
    async def test_put_club(self):
        club = await add_test_club(name='Test Club')
        self.assertEqual(club.name, 'Test Club')

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'name': 'Edited Test Club'}
            response = await async_client.put(f'/club/{club.id}', json=data)
        self.assertEqual(response.status_code, 200)
        edited_club = await get_club_by_filters(id=club.id)
        self.assertEqual(edited_club.name, 'Edited Test Club')
    
    @authenticated_user(app, 'admin')
    async def test_delete_student(self):
        club = await add_test_club(name='Deleted Club')
        self.assertFalse(club.deleted)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/club/{club.id}')
        self.assertEqual(response.status_code, 200)
        deleted_club = await get_club_by_filters(id=club.id)
        self.assertTrue(deleted_club.deleted)
