from datetime import datetime

class Message:
    def __init__(
        self,
        id: int | None,
        chat_session_id: int,
        sender_id: int | None,
        sender_name: str | None,
        role: str,
        content: str,
        timestamp: datetime
    ):

        self.id = id
        self.chat_session_id = chat_session_id
        self.sender_id = sender_id
        self.sender_name = sender_name
        self.role = role
        self.content = content
        self.timestamp = timestamp
