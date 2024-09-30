import asyncio
from typing import AsyncGenerator, Generator, Any
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import NullPool, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.config import DB_NAME_TEST, DB_PORT_TEST, DB_HOST_TEST, DB_PASS_TEST, DB_USER_TEST, DB_NAME, DB_PORT, \
    DB_HOST, DB_PASS, DB_USER
from app.service import prepare_app
from app.storages.database import get_async_session
from app.storages.models import ProductOrm
from app.storages.models.base_model import BaseOrm

app: FastAPI = prepare_app()
base_url: str = 'http://test'
metadata: MetaData = BaseOrm.metadata

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture
async def product_storage():
    """Создает тестовые данные."""
    order = ProductOrm(
        name='Iphone 15 pro max',
        description='Mobile phone',
        price=3100.0,
        quantity=100,
    )
    async with async_session_maker() as session, session.begin():
        session.add(order)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def anyio_backend():
    """Указывает `anyio` какой бэкенд использовать."""
    return 'asyncio'


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, Any, None]:
    """Создает отдельный цикл событий для производства тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop


@pytest.fixture(scope="package")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=base_url) as test_client:
        yield test_client
