import httpx
from config.settings import settings

async def embed_text(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": settings.EMBEDDING_MODEL,
                "prompt": text
            }
        )

    data = response.json()
    return data["embedding"]
