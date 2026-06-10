from datetime import datetime


class ChatSession:
    def __init__(self, id: int | None, user_id: int, title: str, created_at: datetime, updated_at: datetime):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at


