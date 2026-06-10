from datetime import datetime
from sqlalchemy import select
import httpx
from messages.infrastructure.db.message_model import MessageModel
from messages.domain.entities.message import Message
from sqlalchemy.ext.asyncio import AsyncSession



class MessageRepoImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, msg: Message):

        model = MessageModel(
            id=msg.id,
            chat_session_id=msg.chat_session_id,
            sender_id=msg.sender_id,
            sender_name=msg.sender_name,
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp
        )

        self.session.add(model)
        await self.session.commit()

        return Message(
            id=model.id,
            chat_session_id=model.chat_session_id,
            sender_id=model.sender_id,
            sender_name=model.sender_name,
            role=model.role,
            content=model.content,
            timestamp=model.timestamp)


    async def get_history(self, chat_session_id: int, limit: int = 20):

        stmt = (
            select(MessageModel)
            .where(MessageModel.chat_session_id == chat_session_id)
            .order_by(MessageModel.timestamp.asc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        # Convert ORM models → domain entities
        return [
            Message(
                id=row.id,
                chat_session_id=row.chat_session_id,
                role=row.role,
                sender_id=row.sender_id,
                sender_name=row.sender_name,
                content=row.content,
                timestamp=row.timestamp
            )
            for row in rows
        ]


