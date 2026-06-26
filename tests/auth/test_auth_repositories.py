import pytest
import pytest_asyncio
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from auth.infrastructure.repositories.user_repo_impl import UserRepoImpl
from auth.infrastructure.repositories.token_repo_impl import TokenRepoImpl

from auth.domain.entities.user import User
from auth.domain.entities.token import RefreshToken

from auth.infrastructure.db.user_model import UserModel
from auth.infrastructure.db.token_model import RefreshTokenModel

from auth.domain.services.token_services import hash_token, create_refresh_token


Base = declarative_base()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(UserModel.metadata.create_all)
        await conn.run_sync(RefreshTokenModel.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as s:
        yield s


@pytest.mark.asyncio
async def test_user_save(session: AsyncSession):
    repo = UserRepoImpl(session)
    print("auth test hit")

    user = User(
        id=None,
        username="ants",
        email="ants@example.com",
        password_hash="hashed_pw",
    )

    saved = await repo.save(user)

    assert saved.id is not None
    assert saved.username == "ants"
    assert saved.email == "ants@example.com"


@pytest.mark.asyncio
async def test_find_by_username(session: AsyncSession):
    repo = UserRepoImpl(session)

    user = User(
        id=None,
        username="ants",
        email="ants@example.com",
        password_hash="pw",
    )
    await repo.save(user)

    found = await repo.find_by_username("ants")
    assert found is not None
    assert found.username == "ants"


@pytest.mark.asyncio
async def test_find_by_email(session: AsyncSession):
    repo = UserRepoImpl(session)

    user = User(
        id=None,
        username="ants",
        email="ants@example.com",
        password_hash="pw",
    )
    await repo.save(user)

    found = await repo.find_by_email("ants@example.com")
    assert found is not None
    assert found.email == "ants@example.com"


@pytest.mark.asyncio
async def test_find_by_id(session: AsyncSession):
    repo = UserRepoImpl(session)

    user = User(
        id=None,
        username="ants",
        email="ants@example.com",
        password_hash="pw",
    )
    saved = await repo.save(user)

    found = await repo.find_by_id(saved.id)
    assert found is not None
    assert found.id == saved.id


@pytest.mark.asyncio
async def test_update_password_username(session: AsyncSession):
    repo = UserRepoImpl(session)

    user = User(
        id=None,
        username="ants",
        email="ants@example.com",
        password_hash="pwpwpw1",
    )
    saved = await repo.save(user)

    updated = User(
        id=saved.id,
        username="new_ants",
        email=saved.email,
        password_hash="new_pw",
    )

    result = await repo.update_password_username(updated)

    assert result.username == "new_ants"
    assert result.password_hash == "new_pw"
    assert result.email == "ants@example.com"
