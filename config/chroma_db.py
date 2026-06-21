import chromadb
from sentence_transformers import SentenceTransformer
import uuid
from config.settings import settings
import os
from llm.embedder import embed_text


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)



def store_vector(doc_id: str, embedding: list[float], text: str, metadata: dict):
    print("Store vector:", doc_id)
    collection.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata]
    )


async def search_vectors(query: str, k: int = 3):

    query_embedding = await embed_text(query)

    all_docs = collection.get(include=["embeddings"])
    print("stored dims:", [len(e) for e in all_docs["embeddings"]])

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]




def count_vectors():
    return collection.count()


if __name__ == "__main__":
    print("TOTAL VECTORS:", count_vectors())
