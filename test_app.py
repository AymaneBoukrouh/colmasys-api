#! /usr/bin/env python
from test_data import create_test_data
from tests.utils.user import add_test_user
from colmasys import app, get_async_session
from colmasys.core import auth_required
from colmasys.models import Model, Account
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import asyncio
import jwt
import os

### environment variables
load_dotenv()
DB_USER = os.environ['DEMO_DB_USER']
DB_PASS = os.environ['DEMO_DB_PASS']
DB_HOST = os.environ['DEMO_DB_HOST']
DB_NAME = os.environ['DEMO_DB_NAME']
URI = f'mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

### database
async def get_async_session_test():
    engine = create_async_engine(URI)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        yield async_session
    finally:
        await engine.dispose()

app.dependency_overrides[get_async_session] = get_async_session_test
app.dependency_overrides[auth_required.auth_required] = lambda: 1
app.dependency_overrides[auth_required.admin_auth_required] = lambda: 1

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', '*:*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


### data
async def main():
    await reset_and_synchronise_database()
    await create_test_data()

async def reset_and_synchronise_database():
    engine = create_async_engine(URI)
    async with engine.begin() as connection:
        await connection.run_sync(Model.metadata.drop_all) 
        await connection.run_sync(Model.metadata.create_all)
    await engine.dispose()

### main
if __name__ == '__main__':
    asyncio.run(main())
