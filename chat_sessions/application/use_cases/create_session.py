from chat_sessions.domain.interfaces.chat_session_repo import ChatSessionRepository


class CreateChatSessionUseCase:
    def __init__(self, repo:  ChatSessionRepository):
        self.repo = repo

    async def execute(self, user_id: int, title: str):

        await self.repo.create_session(user_id, title)
        return



