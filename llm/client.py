import httpx
from config.settings import settings
import httpx
from config.settings import settings
import asyncio


async def chat_with_llm(prompt: str):
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": settings.LLM_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
    except Exception as e:
        print("LLM crashed:", e)
        raise RuntimeError(f"LLM request failed: {e}")

    data = response.json()

    if "error" in data:
        raise RuntimeError(f"Ollama error: {data['error']}")

    return data["response"].strip()

