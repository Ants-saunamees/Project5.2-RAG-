from ingestion.chunking_rules import CHUNKING_RULES


def chunker(text: str, department: str):
    rules = CHUNKING_RULES[department]

    chunk_size = rules["size"]
    overlap = rules["overlap"]

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        yield chunk
        start = end - overlap
