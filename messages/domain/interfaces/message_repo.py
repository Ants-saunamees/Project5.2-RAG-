from abc import ABC, abstractmethod

class MessageRepository(ABC):

    @abstractmethod
    async def save(self, session_id: str, role: str, content: str):
        pass

    @abstractmethod
    async def get_history(self, session_id: str, limit: int = 20):
        pass
