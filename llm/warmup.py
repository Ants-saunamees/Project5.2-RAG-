import httpx
from config.settings import settings

async def warmup_llm():
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": settings.LLM_MODEL, "prompt": "warm up", "stream": False}
            )

        data = response.json()

        print("🔥 LLM warmed up")

        # Safely print response if it exists

    except Exception as e:
        print("⚠️ LLM warmup failed:", e)
