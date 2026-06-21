import httpx
from config.settings import settings

async def warmup_llm():
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": settings.LLM_MODEL,
                    "prompt": "warm up prompt for LLM",
                    "stream": False
                }
            )

        data = response.json()

        # If Ollama returned an error JSON
        if "error" in data:
            print("⚠️ LLM warmup error from Ollama:", data["error"])
            return

        # If Ollama returned a normal response
        if "response" in data:
            print("🔥 LLM warmed up successfully")
            return

        # Unexpected JSON format
        print("ℹ️ Warmup returned unexpected data:", data)

    except Exception as e:
        print("⚠️ LLM warmup failed:", str(e))
