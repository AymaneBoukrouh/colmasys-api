from tests import URI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

class AsyncTestSession:
    async def __aenter__(self):
        self.engine = create_async_engine(URI)
        async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        return async_session()

    async def __aexit__(self, type, value, traceback):
        await self.engine.dispose()
