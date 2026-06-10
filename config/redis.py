import redis.asyncio as redis
from redis.commands.search.field import VectorField, TextField
import numpy as np
import json
from config.settings import settings

# -----------------------------
# Redis connection
# -----------------------------
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=False
)

# -----------------------------
# Create vector index (HNSW)
# -----------------------------
async def create_index():
    try:
        await redis_client.ft(settings.REDIS_VECTOR_INDEX).info()
        return  # index already exists
    except Exception:
        pass

    await redis_client.ft(settings.REDIS_VECTOR_INDEX).create_index(
        fields=[
            VectorField(
                "vector",
                "HNSW",
                {
                    "TYPE": "FLOAT32",
                    "DIM": settings.VECTOR_DIM,
                    "DISTANCE_METRIC": "COSINE"
                }
            ),
            TextField("text"),
            TextField("department")
        ]
    )

# -----------------------------
# Store a vector + metadata
# -----------------------------
async def store_vector(doc_id: str, embedding: list[float], text: str, metadata: dict):
    vector_bytes = np.array(embedding, dtype=np.float32).tobytes()

    key = f"doc:{doc_id}"

    await redis_client.hset(
        key,
        mapping={
            "vector": vector_bytes,
            "text": text,
            "department": metadata.get("department", "unknown"),
            "meta": json.dumps(metadata)
        }
    )

    return key

# -----------------------------
# KNN Search
# -----------------------------
async def search_vectors(query_embedding: list[float], k: int = 5):
    query_vec = np.array(query_embedding, dtype=np.float32).tobytes()

    q = f'*=>[KNN {k} @vector $vec AS score]'

    results = await redis_client.ft(settings.REDIS_VECTOR_INDEX).search(
        q,
        query_params={"vec": query_vec},
        sort_by="score",
        return_fields=["text", "meta", "score"],
    )

    return results.docs

