from ingestion.loaders import loader
from config.redis import create_index, store_vector
from ingestion.chunker import chunker
from llm.embedder import embed_text
import uuid
import asyncio


async def pipeline(department: str):
    result = loader(department)

    await create_index()

    for chunk in chunker(result["text"], result["department"]):
        id = uuid.uuid4()

        embedding = await embed_text(chunk)

        await store_vector(id, embedding, chunk, result["metadata"])


if __name__ == "__main__":
    asyncio.run(pipeline("pets"))
