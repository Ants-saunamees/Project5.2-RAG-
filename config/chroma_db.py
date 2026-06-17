import chromadb
from sentence_transformers import SentenceTransformer
import uuid

CHROMA_PATH = "./chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

embedder = SentenceTransformer(EMBED_MODEL)



def store_vector(doc_id: str, embedding: list[float], text: str, metadata: dict):
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
