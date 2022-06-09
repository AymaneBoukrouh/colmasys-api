from tests.test_apps.auth_app import testapp as app
from tests.utils.dependencies import get_async_session_test, get_account_id_by_username, raise_jwt_expired_signature_error
from colmasys import auth, get_async_session
from colmasys.models import Account
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class TokenTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    async def test_valid_token(self):
        test_account_id = await get_account_id_by_username('user')
        token = auth.encode_token(test_account_id, Account.Type.Admin)
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            headers = {'Authorization': f'Bearer {token}'}
            response = await async_client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
    
    async def test_invalid_token(self):
        test_account_id = await get_account_id_by_username('user')
        token = auth.encode_token(test_account_id, Account.Type.Admin)[:-4] + 'test'
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            headers = {'Authorization': f'Bearer {token}'}
            response = await async_client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Invalid Token'})

    @raise_jwt_expired_signature_error(app)
    async def test_token_signature_expired(self):
        test_account_id = await get_account_id_by_username('user')
        token = auth.encode_token(test_account_id, Account.Type.Admin)
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            headers = {'Authorization': f'Bearer {token}'}
            response = await async_client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Signature Expired'})
