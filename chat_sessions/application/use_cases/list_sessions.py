from chat_sessions.domain.interfaces.chat_session_repo import ChatSessionRepository


class ListSessionsUseCase:
    def __init__(self, repo: ChatSessionRepository):
        self.repo = repo


    async def execute(self, user_id: int):

        sessions = await self.repo.list_sessions(user_id)

        return sessions
