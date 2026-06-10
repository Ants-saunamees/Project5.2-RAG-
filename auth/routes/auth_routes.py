from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.templating import Jinja2Templates
from auth.application.use_cases.register_user import RegisterUserUseCase
from auth.application.use_cases.login_user import LoginUserUseCase
from config.provider import get_token_repo, get_user_repo
from auth.domain.services.auth_services import is_email

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    user_repo = Depends(get_user_repo),
    token_repo = Depends(get_token_repo),
):
    use_case = RegisterUserUseCase(user_repo, token_repo)

    try:
        result = await use_case.execute(username, email, password)

    except Exception as e:
        return {"error": str(e)}

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 15
    )


    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * 30
    )

    return {
        "success": True,
        "access_token": result["access_token"],
        "user": {
            "id": result["user"].id,
            "username": result["user"].username,
            "email": result["user"].email
        }
    }




@router.post("/login")
async def login(
    response: Response,
    identifier: str = Form(...),
    password: str = Form(...),
    user_repo = Depends(get_user_repo),
    token_repo = Depends(get_token_repo)
):
    use_case = LoginUserUseCase(user_repo, token_repo)

    try:
        result = await use_case.execute(identifier, password)
    except Exception as e:
        return {"error": str(e)}

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 15
    )

    # Set refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,  # <-- FIX
        samesite="lax",
        max_age=60 * 60 * 24 * 30
    )


    return {
        "success": True,
        "access_token": result["access_token"],
        "user": {
            "id": result["user"].id,
            "username": result["user"].username,
            "email": result["user"].email
        }
    }

