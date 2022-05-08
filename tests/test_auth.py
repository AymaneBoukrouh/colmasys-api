from tests.test_apps.auth_app import testapp as app
from tests.utils.dependencies import get_async_session_test, authenticated_user
from colmasys import get_async_session
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class AuthTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    async def test_unprotected_endpoint(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/unprotected')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

    async def test_protected_forbidden_endpoint(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/protected')
        self.assertEqual(response.status_code, 403)
    
    @authenticated_user(app)
    async def test_protected_authorized_endpoint(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/protected')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
