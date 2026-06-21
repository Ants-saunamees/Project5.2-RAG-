import httpx
from config.settings import settings
from llm.client import chat_with_llm


async def query_rewriter(history, question: str) -> str:
    # Convert history into readable text
    history_text = ""
    for msg in history:
        history_text += f"{msg.role}: {msg.content}\n"

    prompt = f"""
Rewrite the user's question into a standalone query.

Chat History:
{history_text}

User Question:
{question}

Rules:
- Keep the meaning the same.
- Resolve pronouns like "it", "that", "this", "he", "she".
- Make it a complete question.
- Do NOT answer the question.
- Only output the rewritten question.
"""

    # ⭐ FIX: await the LLM call
    llm_raw = await chat_with_llm(prompt)

    # chat_with_llm already returns the text, so just return it
    return llm_raw.strip()