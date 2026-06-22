from fastapi import APIRouter, Depends, Form
from config.provider import get_message_repo
from api.auth_required.auth_required import auth_required
from llm.query_rewriter import query_rewriter
from llm.client import chat_with_llm
from llm.embedder import embed_text
from config.chroma_db import search_vectors

router = APIRouter(prefix="/llm", tags=["LLM"])



@router.post("/llm_answer")
async def llm_answer(
    session_id: int = Form(...),
    question: str = Form(...),
    repo = Depends(get_message_repo),
    user = Depends(auth_required)
):
    # 1. Load chat history
    try:
        history = await repo.get_history(session_id)
    except Exception as e:
        return {"error": f"failed to load history: {e}"}

    # 2. Rewrite the question
    try:
        rewritten = await query_rewriter(history, question)
    except Exception as e:
        return {"error": f"query rewriter failed: {e}"}

    # 4. Retrieve top-k chunks from Redis
    try:
        docs = await search_vectors(rewritten, user.department, k=5)
    except Exception as e:
        return {"error": f"vector search failed: {e}"}

    # 5. Build context
    try:
        context = "\n\n".join(docs)
    except Exception as e:
        return {"error": f"context building failed: {e}"}

    # 6. Build final prompt
    prompt = f"""
Use ONLY the context below to answer the question.
If the answer is not in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Rewritten Question:
{rewritten}

Answer:
"""

    # 7. Get LLM answer
    try:
        answer = await chat_with_llm(prompt)
    except Exception as e:
        return {"error": f"LLM answer failed: {e}"}

    return {"answer": answer.strip()}
