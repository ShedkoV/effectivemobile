from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    url='postgresql+asyncpg://shedko:postgres@localhost:5432/effective_warehouse',
    echo=True,
    pool_pre_ping=True,
)

async_session = sessionmaker(  # type: ignore[call-overload]
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Getting a session to connect to the database."""
    async with async_session() as session:
        yield session
