from config.redis import search_vectors
from ingestion.embedder import embedder


async def retrieve_chunks(q: str, n_results: int = 5):
    # Get embedding vector only
    embedding_result = await embedder(q)
    q_embedding = embedding_result["vector"]

    # Search Redis for similar chunks
    chunks = await search_vectors(q_embedding, n_results)

    return chunks



