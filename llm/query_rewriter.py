import httpx
from config.settings import settings

async def query_rewriter(history, question: str) -> str:
    """
    Rewrites the user's question into a standalone query using chat history.
    Accepts a list of Message objects (not dicts).
    """

    # Convert history into readable text
    history_text = ""
    for msg in history:
        # msg is a Message object → use attributes, not dict keys
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

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

    data = response.json()
    print("REWRITER RAW RESPONSE:", data)

    if "error" in data:
        raise ValueError(f"LLM error: {data['error']}")

    if "response" not in data:
        raise ValueError(f"Unexpected LLM output: {data}")

    return data["response"].strip()