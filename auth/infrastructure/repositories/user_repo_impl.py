from sqlalchemy.orm import Session
from auth.domain.interfaces.user_repo import UserRepository
from auth.domain.entities.user import User
from auth.infrastructure.db.user_model import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepoImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def save(self, user: User):

        model = UserModel(
            id=None,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            department=user.department
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            department=model.department
        )

    async def find_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            department=model.department
        )

    async def find_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            department=model.department
        )

    async def find_by_id(self, id: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            department=model.department
        )