import httpx

from config.settings import settings


async def embedder(text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": settings.EMBEDDER_MODEL,
                "prompt": text
            }
        )

    data = response.json()

    # Ollama returns: { "embedding": [vector] }
    return data["embedding"]