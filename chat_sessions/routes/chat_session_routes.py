from fastapi import APIRouter, Depends, Form
from api.auth_required.auth_required import auth_required
from config.provider import get_chat_session_repo
from chat_sessions.application.use_cases.delete_session import DeleteChatSessionUseCase
from chat_sessions.application.use_cases.create_session import CreateChatSessionUseCase
from chat_sessions.application.use_cases.list_sessions import ListSessionsUseCase
from chat_sessions.application.use_cases.update_title import UpdateTitleUseCase

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/create_session")
async def create_session(
        title: str = Form(...),
        repo = Depends(get_chat_session_repo),
        user = Depends(auth_required)):

    use_case = CreateChatSessionUseCase(repo)


    try:
        await use_case.execute(user.id, title)
    except Exception as e:
        return {"error": str(e)}

    return {"success": True}

@router.get("/list_sessions")
async def list_sessions(
        repo = Depends(get_chat_session_repo),
        user = Depends(auth_required)):

    use_case = ListSessionsUseCase(repo)

    try:
        sessions = await use_case.execute(user.id)
    except Exception as e:
        return {"error": str(e)}
    return {"success": True, "sessions": sessions}


@router.delete("/delete_session")
async def delete_session(
        session_id: int,
        repo = Depends(get_chat_session_repo),
        user = Depends(auth_required)):

    use_case = DeleteChatSessionUseCase(repo)
    try:
        await use_case.execute(user.id, session_id)
    except Exception as e:
        return {"error": str(e)}
    return {"success": True}


@router.patch("/update_title")
async def update_title(
        session_id: int,
        new_title: str,
        repo = Depends(get_chat_session_repo),
        user = Depends(auth_required)):
    use_case = UpdateTitleUseCase(repo)

    try:
        await use_case.execute(session_id, user.id, new_title)
    except Exception as e:
        return {"error": str(e)}
    return {"success": True}






