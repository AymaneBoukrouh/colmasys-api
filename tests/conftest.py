from tests import URI
from tests.utils.user import add_test_user
from tests.utils.class_ import add_test_class
from colmasys.models import Model, User
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

def pytest_configure():
    asyncio.run(main())

async def main():
    await reset_and_synchronise_database()
    await create_test_users()
    await create_test_classes()

async def reset_and_synchronise_database():
    engine = create_async_engine(URI)
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all) 
        await connection.run_sync(Model.metadata.create_all)
    await engine.dispose()

async def create_test_users():
    await add_test_user(username='user', password='pass')
    await add_test_user(user_type=User.Type.admin, username='admin', password='admin')
    await add_test_user(user_type=User.Type.professor, username='professor', password='admin')
    await add_test_user(user_type=User.Type.student, username='student', password='student')

async def create_test_classes():
    for i in range(4):
        await add_test_class(academic_year='2021/2022', year=1, group=i+1, major='AP')
    await add_test_class(academic_year='2021/2022', year=3, group=1, major='IIR')
    await add_test_class(academic_year='2021/2022', year=3, group=2, major='IIR')
