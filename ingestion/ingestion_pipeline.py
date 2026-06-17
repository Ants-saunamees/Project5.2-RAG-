from ingestion.loaders import loader
from ingestion.chunker import chunker
from llm.embedder import embed_text
from config.chroma_db import store_vector, collection
import uuid
import asyncio

async def pipeline(department: str):
    for result in loader(department):
        for chunk in chunker(result["text"], result["metadata"]["department"]):
            doc_id = str(uuid.uuid4())
            embedding = await embed_text(chunk)
            store_vector(doc_id, embedding, chunk, result["metadata"]) # prg peab koik reingestima kui addid juurde

    # AFTER ingestion is done
    print("Flushing DB...")
    print("Final count:", collection.count())


if __name__ == "__main__":
    asyncio.run(pipeline("pets"))
