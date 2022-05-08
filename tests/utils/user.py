from tests.utils.db import AsyncTestSession
from colmasys import auth
from colmasys.models import User
from sqlalchemy import select
from datetime import datetime

async def get_user_by_filters(**kwargs) -> User:
    async with AsyncTestSession() as session, session.begin():
        query = select(User).filter_by(**kwargs)
        result = await session.execute(query)
        user = result.scalars().first()
    return user

async def get_user_id_by_username(username):
    user = await get_user_by_filters(username=username)
    return user.id

def generate_test_user_data(**kwargs):
    username = kwargs['username']
    default_values = {
        'firstname': username, 'lastname': username, 'username': username,
        'email': f'{username}@domain.com', 'password': username,
        'birthdate': '01/01/2000', 'gender': 1, 'user_type': 0
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
        user = User(**data)
        session.add(user)
        await session.commit()
    return user