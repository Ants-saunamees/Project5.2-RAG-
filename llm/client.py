import httpx
from config.settings import settings
import httpx
from config.settings import settings

async def chat_with_llm(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/generate",
            json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

    data = response.json()
    return data["response"].strip()
