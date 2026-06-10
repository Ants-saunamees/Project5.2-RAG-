from chat_sessions.domain.interfaces.chat_session_repo import ChatSessionRepository


class UpdateTitleUseCase:
    def __init__(self, repo: ChatSessionRepository):
        self.repo = repo


    async def execute(self, session_id, user_id: int, new_title: str):

        result = await self.repo.update_title(session_id, user_id, new_title)

        if result is False:
            raise Exception("Failed to update title")

        return