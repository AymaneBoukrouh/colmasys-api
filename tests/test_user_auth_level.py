from tests.test_apps.auth_app import testapp as app
from tests.utils.dependencies import get_async_session_test, get_account_id_by_username
from colmasys import auth, get_async_session
from colmasys.models import Account
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class UserAuthLevelTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]
    
    async def get_as_user(self, endpoint, username):
        test_account_id = await get_account_id_by_username(username)
        token = auth.encode_token(test_account_id, getattr(Account.Type, username.capitalize()))
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            headers = {'Authorization': f'Bearer {token}'}
            response = await async_client.get(endpoint, headers=headers)
        return response

    async def assert_authorized(self, endpoint, usernames):
        for username in usernames:
            response = await self.get_as_user(endpoint, username)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'status': 'success'})

    async def assert_unauthorized(self, endpoint, usernames):
        for username in usernames:
            response = await self.get_as_user(endpoint, username)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json(), {'detail': 'Permission Denied'})
        
    async def test_any_user_endpoint(self):
        await self.assert_authorized('/any_user', ['admin', 'professor', 'student'])

    async def test_admin_endpoint(self):
        await self.assert_authorized('/admin_only', ['admin'])
        await self.assert_unauthorized('/admin_only', ['professor', 'student'])

    async def test_professor_endpoint(self):
        await self.assert_authorized('/professor_only', ['professor'])
        await self.assert_unauthorized('/professor_only', ['admin', 'student'])

    async def test_student_endpoint(self):
        await self.assert_authorized('/student_only', ['student'])
        await self.assert_unauthorized('/student_only', ['admin', 'professor'])
