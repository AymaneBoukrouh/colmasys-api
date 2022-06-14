from tests.utils.db import AsyncTestSession
from tests.utils.class_ import get_class_by_filters, add_test_class
from tests.utils.dependencies import get_async_session_test, authenticated_user
from tests.utils.user import get_account_by_filters
from colmasys import app, get_async_session
from sqlalchemy import select 
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class ChatTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    #@authenticated_user(app, 'admin')
    #async def test_post_class(self):
    #    data = {'academic_year': '2022/2023', 'year': 3, 'group': 2, 'major': 'IIR'}
    #    async with AsyncClient(app=app, base_url='http://localhost') as async_client:
    #        response = await async_client.post('/class', json=data)
    #    self.assertEqual(response.status_code, 201)
#
    #    class_ = await get_class_by_filters(**data)
    #    self.assertIsNotNone(class_)
#
    #    async with AsyncClient(app=app, base_url='http://localhost') as async_client:
    #        response = await async_client.post('/class', json=data)
    #    self.assertEqual(response.status_code, 409)
    #    self.assertEqual(response.json(), {'detail': 'Class Already Exists'})
#
    @authenticated_user(app, username='user')
    async def test_get_chats(self):
        user = await get_account_by_filters(username='user')
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/chats')
        self.assertEqual(response.status_code, 200)
        user_chat_ids = [chat.id for chat in user.chats]
        response_chat_ids = [chat['id'] for chat in response.json()]
        self.assertEqual(set(user_chat_ids), set(response_chat_ids))

