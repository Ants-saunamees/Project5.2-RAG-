import secrets
from datetime import datetime, timedelta
from auth.domain.services.token_services import create_refresh_token


class RefreshToken:
    def __init__(
        self,
        id: int | None,
        user_id: int,
        token: str,
        expires_at: datetime,
        created_at: datetime | None,
        revoked: bool = False,
    ):
        if len(token) < 32:
            raise ValueError("Token too short")

        self.id = id
        self.token = token
        self.user_id = user_id
        self.expires_at = expires_at
        self.created_at = created_at
        self.revoked = revoked

    @staticmethod
    def create(user_id: int, ttl_minutes: int = 60 * 24 * 7):
        token = create_refresh_token()
        expires = datetime.utcnow() + timedelta(minutes=ttl_minutes)

        return RefreshToken(
            id=None,
            token=token,
            user_id=user_id,
            expires_at=expires,
            created_at=datetime.utcnow(),
            revoked=False
        )
