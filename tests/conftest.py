from tests import URI
from tests.utils.user import add_test_user, get_account_by_filters
from tests.utils.class_ import add_test_class
from tests.utils.post import add_test_post, get_post_by_filters
from tests.utils.comment import add_test_comment
from colmasys.models import Model, Account
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

def pytest_configure():
    asyncio.run(main())

async def main():
    await reset_and_synchronise_database()
    await create_test_users()
    await create_test_classes()
    await create_test_posts()
    await create_test_comments()

async def reset_and_synchronise_database():
    engine = create_async_engine(URI)
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all) 
        await connection.run_sync(Model.metadata.create_all)
    await engine.dispose()

async def create_test_users():
    await add_test_user(username='user', password='pass')
    await add_test_user(username='random_user', password='random_pass')
    await add_test_user(account_type=Account.Type.Admin, username='admin', password='admin')
    await add_test_user(account_type=Account.Type.Professor, username='professor', password='admin')
    await add_test_user(account_type=Account.Type.Student, username='student', password='student')

async def create_test_classes():
    for i in range(4):
        await add_test_class(academic_year='2021/2022', year=1, group=i+1, major='AP')
    await add_test_class(academic_year='2021/2022', year=3, group=1, major='IIR')
    await add_test_class(academic_year='2021/2022', year=3, group=2, major='IIR')

async def create_test_posts():
    await add_test_post(
        title = 'Post Title',
        content = 'Post content.',
        author = await get_account_by_filters(username='user')
    )

async def create_test_comments():
    post = await get_post_by_filters(title='Post Title')

    await add_test_comment(
        content = 'Post comment.',
        author = post.author,
        post = post
    )