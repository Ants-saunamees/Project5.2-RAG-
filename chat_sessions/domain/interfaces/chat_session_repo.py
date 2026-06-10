from abc import ABC, abstractmethod


class ChatSessionRepository(ABC):
    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def list_sessions(self):
        pass

    @abstractmethod
    def update_title(self):
        pass

    @abstractmethod
    def delete_session(self):
        pass

