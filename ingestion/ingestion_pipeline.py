from ingestion.loaders import loader
from ingestion.chunker import chunker
from llm.embedder import embed_text
from config.chroma_db import store_vector
import asyncio
import uuid

async def pipeline(department: str):
    for result in loader(department):   # iterate the generator
        print("1")

        # no index creation needed for Chroma
        print("2")

        for chunk in chunker(result["text"], result["metadata"]["department"]):
            id = str(uuid.uuid4())
            print("3")

            embedding = await embed_text(chunk)
            print("4")

            store_vector(id, embedding, chunk, result["metadata"])

if __name__ == "__main__":
    asyncio.run(pipeline("pets"))
