from fastapi import Request, HTTPException, Depends
from config.database import get_session
from auth.domain.services.token_services import (
    verify_access_token,
    create_access_token
)
from auth.infrastructure.repositories.token_repo_impl import TokenRepoImpl
from auth.infrastructure.repositories.user_repo_impl import UserRepoImpl


def get_token_from_request(request: Request):
    access = request.cookies.get("access_token")
    refresh = request.cookies.get("refresh_token")
    return access, refresh


def validate_access(access_token: str):
    if not access_token:
        return None
    try:
        payload = verify_access_token(access_token)

        return payload.get("user_id")

    except Exception:
        return None

def validate_refresh(refresh_token: str):
    if not refresh_token:
        return None
    token_record = TokenRepoImpl.find_by_token(refresh_token)
    if not token_record:
        return None
    return token_record.user_id



async def attach_user_to_request(request: Request, user_id: int, session):
    repo = UserRepoImpl(session)
    user = await repo.find_by_id(user_id)
    request.state.user = user
    return user



def issue_new_access_token(user_id: int):
    return create_access_token({"sub": str(user_id)})

