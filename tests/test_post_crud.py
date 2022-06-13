from tests.utils.db import AsyncTestSession
from tests.utils.dependencies import get_async_session_test, authenticated_user
from tests.utils.user import get_account_by_filters
from tests.utils.post import get_post_by_filters
from colmasys import app, get_async_session
from colmasys.models import Account
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class PostTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, username='student')
    async def test_post_post(self):
        student = await get_account_by_filters(username='student')
        self.assertEqual(len(student.posts), 0)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'title': 'Test Title', 'content': 'Test content.'}
            response = await async_client.post(f'/post', json=data)
        self.assertEqual(response.status_code, 201)

        student = await get_account_by_filters(username='student')
        self.assertEqual(len(student.posts), 1)
        self.assertEqual(student.posts[0].title, data['title'])

    @authenticated_user(app, username='user')
    async def test_get_user_posts(self):
        user = await get_account_by_filters(username='user')
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/user/{user.username}/posts')
        self.assertEqual(response.status_code, 200)
        user_post_ids = [post.id for post in user.posts]
        response_post_ids = [post['id'] for post in response.json()]
        self.assertEqual(set(user_post_ids), set(response_post_ids))

    @authenticated_user(app, username='user')
    async def test_get_post(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), post.serialize())

    @authenticated_user(app, username='user')
    async def test_get_inexistent_post(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/post/1000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Post Not Found'})

    @authenticated_user(app, username='user')
    async def test_put_post_authorized(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)
        self.assertEqual(post.title, 'Post Title')

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'title': 'Edited Post Title'}
            response = await async_client.put(f'/post/{post.id}', json=data)
        self.assertEqual(response.status_code, 200)
        post = await get_post_by_filters(id=post.id)
        self.assertEqual(post.title, 'Edited Post Title')

    @authenticated_user(app, username='random_user')
    async def test_put_post_unauthorized(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'title': 'Random Post Title'}
            response = await async_client.put(f'/post/{post.id}', json=data)
            self.assertEqual(response.status_code, 403)

    @authenticated_user(app, username='user')
    async def test_delete_post_authorized(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        post = await get_post_by_filters(id=post.id)
        self.assertTrue(post.deleted)       

    @authenticated_user(app, username='random_user')
    async def test_delete_post_unauthorized(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/post/{post.id}')
        self.assertEqual(response.status_code, 403)
