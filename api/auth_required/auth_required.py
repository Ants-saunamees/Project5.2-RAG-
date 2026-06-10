from fastapi import Request, Response, Depends, HTTPException
from api.auth_required.auth_required_helpers import (
    get_token_from_request,
    validate_access,
    issue_new_access_token,
    attach_user_to_request
)
from auth.infrastructure.repositories.token_repo_impl import TokenRepoImpl
from config.database import get_session



async def auth_required(
    request: Request,
    response: Response,
    session=Depends(get_session)
):
    token_repo = TokenRepoImpl(session)

    access, refresh = get_token_from_request(request)

    # 1. Try access token
    user_id = validate_access(access)
    if user_id:
        user = await attach_user_to_request(request, user_id, session)
        return user

    # 2. Try refresh token
    db_token = await token_repo.validate_refresh(refresh)   # <-- FIXED await
    if db_token:

        new_raw, new_entity = await token_repo.rotate_refresh_token(db_token)  # <-- FIXED order


        new_access = issue_new_access_token(db_token.user_id)

        response.set_cookie(
            "access_token",
            new_access,
            httponly=True,
            secure=True,
            samesite="strict"
        )
        response.set_cookie(
            "refresh_token",
            new_raw,
            httponly=True,
            secure=True,
            samesite="strict"
        )

        user = await attach_user_to_request(request, db_token.user_id, session)
        return user


    raise HTTPException(401, "Unauthorized")
