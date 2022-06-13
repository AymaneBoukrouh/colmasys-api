from tests import URI
from tests.utils.db import AsyncTestSession
from tests.utils.user import get_account_id_by_username
from colmasys.core import auth_required
from colmasys.models import Account
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
import jwt

### database
async def get_async_session_test():
    engine = create_async_engine(URI)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    try:
        yield async_session
    finally:
        await engine.dispose()

### authentication
async def auth_any(username: str):
    return await get_account_id_by_username(username)

async def auth_admin():
    return await get_account_id_by_username('admin')

async def auth_student():
    return await get_account_id_by_username('student')

def authenticated_user(app, account_type=None, username=None):
    if not account_type:
        auth_level = auth_required.auth_required
        async def tmp_auth():
            return await auth_any(username=username)
        auth_dependency = tmp_auth
    elif account_type == 'admin':
        auth_level = auth_required.admin_auth_required
        auth_dependency = auth_admin
    elif account_type == 'student':
        auth_level = auth_required.student_auth_required
        auth_dependency = auth_student

    def decorator(test_func):
        @wraps(test_func)
        async def wrapper(*args, **kwargs):
            app.dependency_overrides[auth_level] = auth_dependency
            await test_func(*args, **kwargs)
            del app.dependency_overrides[auth_level]
        return wrapper
    return decorator

### token
async def auth_jwt_expired_signature_error():
    raise HTTPException(status_code=401, detail='Signature Expired')

def raise_jwt_expired_signature_error(app):
    def decorator(test_func):
        @wraps(test_func)
        async def wrapper(*args, **kwargs):
            try:
                app.dependency_overrides[auth_required.auth_required] = auth_jwt_expired_signature_error
                await test_func(*args, **kwargs)
            finally:
                del app.dependency_overrides[auth_required.auth_required]
        return wrapper
    return decorator
