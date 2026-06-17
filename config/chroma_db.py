import chromadb
from sentence_transformers import SentenceTransformer
import uuid

EMBED_MODEL = "all-MiniLM-L6-v2"
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

embedder = SentenceTransformer(EMBED_MODEL)



def store_vector(doc_id: str, embedding: list[float], text: str, metadata: dict):
    print("Store vector:", doc_id)
    collection.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )


def search_vectors(query: str, k: int = 5):
    query_embedding = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]


def count_vectors():
    return collection.count()


if __name__ == "__main__":
    print("TOTAL VECTORS:", count_vectors())
