from colmasys.core.auth import Auth, AuthCreds
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

### environment variables
load_dotenv()
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

URI = f'mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

### app
app = FastAPI()
auth = Auth()

### dependencies
async def get_async_session():
    engine = create_async_engine(URI)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        yield async_session
    finally:
        await engine.dispose()

### endpoints
from colmasys.endpoints import *
