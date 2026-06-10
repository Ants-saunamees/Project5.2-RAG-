from fastapi import APIRouter, Depends, Form
from starlette.responses import JSONResponse
from messages.domain.entities.message import Message
from messages.application.use_cases.get_history import GetHistoryUseCase
from messages.application.use_cases.save_message import SaveMessageUseCase
from config.provider import get_message_repo
from api.auth_required.auth_required import auth_required
from messages.infrastructure.repositories.message_repo_impl import MessageRepoImpl
from llm.query_rewriter import query_rewriter
from config.redis import search_vectors
from llm.client import chat_with_llm
from llm.embedder import embed_text


router = APIRouter(prefix="/message", tags=["Message"])


@router.get("/get_history")
async def get_history(session_id: int, repo = Depends(get_message_repo)):
    use_case = GetHistoryUseCase(repo)

    try:
        messages = await use_case.execute(session_id)
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    return messages

@router.post("/save_message")
async def save_message(
        room_id: int = Form(...),
        role: str = Form(...),
        content: str = Form(...),
        repo = Depends(get_message_repo),
        user = Depends(auth_required)
):

    use_case = SaveMessageUseCase(repo)

    try:
        message = await use_case.execute(
            chat_session_id=room_id,
            role=role,
            content=content,
            sender_id=user.id,
            sender_name=user.username,
        )

    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

    return message
