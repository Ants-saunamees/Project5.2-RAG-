import secrets
from datetime import datetime, timedelta
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

import hashlib

from config.settings import settings
from fastapi.responses import JSONResponse


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token():
    return secrets.token_hex(64)  # 64-char random string

def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()



# -----------------------------
# Verify ACCESS token
# -----------------------------
def verify_access_token(token: str):
    """
    Returns payload if valid.
    Raises exception if invalid.
    """
    if not token:
        raise InvalidTokenError("Missing access token")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except ExpiredSignatureError:
        # Access token expired → middleware will try refresh token
        raise ExpiredSignatureError("Access token expired")

    except InvalidTokenError:
        raise InvalidTokenError("Invalid access token")
