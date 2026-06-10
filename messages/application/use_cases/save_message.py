import datetime

from messages.domain.interfaces.message_repo import MessageRepository
from messages.domain.entities.message import Message


class SaveMessageUseCase:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    async def execute(
        self,
        chat_session_id: int,
        role: str,
        content: str,
        sender_id: int | None,
        sender_name: str | None
    ):

        msg = Message(
            id=None,
            chat_session_id=chat_session_id,
            sender_id=sender_id,
            sender_name=sender_name,
            role=role,
            content=content,
            timestamp=datetime.datetime.now()
        )

        message = await self.repo.save(msg)

        return message
