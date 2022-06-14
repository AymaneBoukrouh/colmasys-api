from tests.utils.db import AsyncTestSession
from tests.utils.dependencies import get_async_session_test, authenticated_user
from tests.utils.user import get_account_by_filters
from tests.utils.post import get_post_by_filters
from tests.utils.comment import get_comment_by_filters
from colmasys import app, get_async_session
from colmasys.models import Account
from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase

class VoteTest(IsolatedAsyncioTestCase):
    def setUp(self):
        app.dependency_overrides[get_async_session] = get_async_session_test

    def tearDown(self):
        del app.dependency_overrides[get_async_session]

    @authenticated_user(app, username='user')
    async def test_post_post_vote(self):
        user = await get_account_by_filters(username='user')
        post = await get_post_by_filters(id=user.posts[0].id)
        self.assertEqual(len(user.post_votes), 0)

        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            data = {'value': True}
            response = await async_client.post(f'/post/{post.id}/vote', json=data)
        self.assertEqual(response.status_code, 201)

        user = await get_account_by_filters(username='user')
        self.assertEqual(len(user.post_votes), 1)
        self.assertEqual(user.post_votes[0].value, data['value'])

    @authenticated_user(app, username='user')
    async def test_get_comment_votes(self):
        comment = (await get_account_by_filters(username='user')).comments[0]
        comment = await get_comment_by_filters(id=comment.id)
        async with AsyncClient(app=app, base_url='http://localhost') as async_client:
            response = await async_client.get(f'/comment/{comment.id}/votes')
        self.assertEqual(response.status_code, 200)
        comment_vote_ids = [vote.id for vote in comment.votes]
        response_vote_ids = [vote['id'] for vote in response.json()]
        self.assertEqual(set(comment_vote_ids), set(response_vote_ids))
