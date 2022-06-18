from tests.utils.db import AsyncTestSession
from colmasys import auth
from colmasys.models import Account, Student, Professor
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

async def get_account_by_filters(**kwargs) -> Account:
    async with AsyncTestSession() as session, session.begin():
        query = (
            select(Account)
            .filter_by(**kwargs)
        )

        result = await session.execute(query)
        account = result.scalars().first()
    return account

async def get_account_id_by_username(username):
    account = await get_account_by_filters(username=username)
    return account.id

def generate_test_user_data(**kwargs):
    username = kwargs['username']
    default_values = {
        'firstname': username, 'lastname': username, 'username': username,
        'email': f'{username}@domain.com', 'password': username,
        'birthdate': '01/01/2000', 'gender': 1, 'account_type': 0
    }

    fields = default_values.keys()
    data = dict()
    for field in fields:
        data[field] = kwargs[field] if field in kwargs else default_values[field]
    return data


async def add_test_user(**kwargs):
    data = generate_test_user_data(**kwargs)
    for field in data.keys():
        if field == 'password':
            data[field] = auth.hash_password(data[field])
        elif field == 'birthdate':
            data[field] = datetime.strptime(data[field], '%d/%m/%Y')

    async with AsyncTestSession() as session, session.begin():
        account = Account(**data)
        session.add(account)

        await session.commit()
    
    return await get_account_by_filters(id=account.id)

async def add_test_student(class_=None, **kwargs):
    account = await add_test_user(**kwargs)

    async with AsyncTestSession() as session, session.begin():
        student = Student(account=account, class_=class_)
        session.add(student)
        await session.commit()

    return student

async def add_test_professor(**kwargs):
    account = await add_test_user(**kwargs)

    async with AsyncTestSession() as session, session.begin():
        professor = Professor(account=account)
        session.add(professor)
        await session.commit()

    return professor
