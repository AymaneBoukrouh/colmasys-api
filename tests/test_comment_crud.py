from tests.utils.db import AsyncTestSession
from tests.utils.dependencies import get_async_session_test, authenticated_user
from tests.utils.user import get_account_by_filters
from tests.utils.comment import get_comment_by_filters
from tests.utils.post import get_post_by_filters
from colmasys import app, get_async_session
from colmasys.models import Account
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class CommentTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, username='user')
    async def test_post_comment(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'content': 'Test comment.'}
            response = await async_client.post(f'/post/{post.id}/comment', json=data)
        self.assertEqual(response.status_code, 201)
    
    @authenticated_user(app, username='user')
    async def test_get_user_comments(self):
        user = await get_account_by_filters(username='user')
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/user/{user.username}/comments')
        self.assertEqual(response.status_code, 200)
        user_comment_ids = [comment.id for comment in user.comments]
        response_comment_ids = [comment['id'] for comment in response.json()]
        self.assertEqual(set(user_comment_ids), set(response_comment_ids))

    @authenticated_user(app, username='user')
    async def test_get_post_comments(self):
        post = (await get_account_by_filters(username='user')).posts[0]
        post = await get_post_by_filters(id=post.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/post/{post.id}/comments')
        self.assertEqual(response.status_code, 200)
        post_comment_ids = [comment.id for comment in post.comments]
        response_comment_ids = [comment['id'] for comment in response.json()]
        self.assertEqual(set(post_comment_ids), set(response_comment_ids))

    @authenticated_user(app, username='user')
    async def test_get_comment(self):
        comment = (await get_account_by_filters(username='user')).comments[0]
        comment = await get_comment_by_filters(id=comment.id)
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/comment/{comment.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), comment.serialize())

    @authenticated_user(app, username='user')
    async def test_get_inexistent_comment(self):
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get('/comment/1000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Comment Not Found'})

    @authenticated_user(app, username='user')
    async def test_put_comment_authorized(self):
        comment = (await get_account_by_filters(username='user')).comments[0]
        comment = await get_comment_by_filters(id=comment.id)
        self.assertEqual(comment.content, 'Post comment.')

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'content': 'Edited post comment.'}
            response = await async_client.put(f'/comment/{comment.id}', json=data)
        self.assertEqual(response.status_code, 200)
        comment = await get_comment_by_filters(id=comment.id)
        self.assertEqual(comment.content, 'Edited post comment.')

    @authenticated_user(app, username='random_user')
    async def test_put_comment_unauthorized(self):
        comment = (await get_account_by_filters(username='user')).comments[0]
        comment = await get_comment_by_filters(id=comment.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'content': 'Random post content.'}
            response = await async_client.put(f'/comment/{comment.id}', json=data)
            self.assertEqual(response.status_code, 403)

    @authenticated_user(app, username='user')
    async def test_delete_comment_authorized(self):
        comment = (await get_account_by_filters(username='user')).comments[0]
        comment = await get_comment_by_filters(id=comment.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/comment/{comment.id}')
        self.assertEqual(response.status_code, 200)
        comment = await get_comment_by_filters(id=comment.id)
        self.assertTrue(comment.deleted)       

    @authenticated_user(app, username='random_user')
    async def test_delete_comment_unauthorized(self):
        comment = (await get_account_by_filters(username='user')).comments[0]
        comment = await get_comment_by_filters(id=comment.id)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.delete(f'/comment/{comment.id}')
        self.assertEqual(response.status_code, 403)
