from tests.utils.dependencies import get_async_session_test
from colmasys import app, get_async_session
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class LoginTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    async def post_login(self, username, password):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'username': username, 'password': password}
            return await async_client.post('/login', json=data)

    async def test_login_authorized(self):
        response = await self.post_login('user', 'pass')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json().keys())
    
    async def test_login_unauthorized(self):
        response = await self.post_login('random', 'random')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Invalid Username/Password'})

    async def test_login_wrong_password(self):
        response = await self.post_login('user', '')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Invalid Username/Password'})
