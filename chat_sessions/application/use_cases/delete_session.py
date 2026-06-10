from chat_sessions.domain.interfaces.chat_session_repo import ChatSessionRepository


class DeleteChatSessionUseCase:
    def __init__(self, repo: ChatSessionRepository):
        self.repo = repo

    async def execute(self, user_id: int, session_id: int):
        result = await self.repo.delete_session(session_id, user_id)

        if result is False:
            raise Exception("Failed to delete session")

        return