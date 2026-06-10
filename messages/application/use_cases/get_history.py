from messages.domain.interfaces.message_repo import MessageRepository
from messages.infrastructure.repositories.message_repo_impl import MessageRepoImpl


class GetHistoryUseCase:
    def __init__(self, repo: MessageRepository):
        self.repo = repo

    async def execute(self, chat_session_id: int):
        messages = await self.repo.get_history(chat_session_id)
        return messages