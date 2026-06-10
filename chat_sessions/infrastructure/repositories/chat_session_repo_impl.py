from datetime import datetime

from pydantic.v1.datetime_parse import time_expr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from chat_sessions.domain.entities.chat_session import ChatSession
from chat_sessions.domain.interfaces.chat_session_repo import ChatSessionRepository
from chat_sessions.infrastructure.db.chat_session_model import ChatSessionModel

class ChatSessionRepoImpl(ChatSessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_session(self, user_id: int, title: str):

        model = ChatSessionModel(
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return ChatSession(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def list_sessions(self, user_id: int):
        stmt = (
            select(ChatSessionModel)
            .where(ChatSessionModel.user_id == user_id)
            .order_by(ChatSessionModel.updated_at.desc())
        )

        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [
            ChatSession(
                id=row.id,
                user_id=row.user_id,
                title=row.title,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            for row in rows
        ]

    async def delete_session(self, session_id: int, user_id: int):

        stmt = select(ChatSessionModel).where(ChatSessionModel.id == session_id)
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        # Session does not exist
        if row is None:
            return False

        # Session belongs to another user → security check
        if row.user_id != user_id:
            return False

        await self.session.delete(row)
        await self.session.commit()
        return True

    async def update_title(self, session_id: int, user_id: int, new_title: str):

        stmt = select(ChatSessionModel).where(ChatSessionModel.id == session_id)
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if row is None:
            return False

        if row.user_id != user_id:
            return False

        row.title = new_title
        await self.session.commit()

        return True






