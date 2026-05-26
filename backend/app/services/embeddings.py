from typing import List
from dashscope import TextEmbedding
from app.config import settings

BATCH_SIZE = 10


class EmbeddingService:
    """Generate embeddings using 百炼 Embedding v3."""

    def __init__(self):
        self.model = settings.embedding_model
        self.api_key = settings.dashscope_api_key

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        all_embeddings = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            resp = TextEmbedding.call(
                model=self.model,
                input=batch,
                api_key=self.api_key,
            )

            if resp.status_code != 200:
                raise RuntimeError(f"Embedding API error: {resp.code} - {resp.message}")

            for emb in resp.output.get("embeddings", []):
                all_embeddings.append(emb["embedding"])

        return all_embeddings

    def embed_single(self, text: str) -> List[float]:
        embeddings = self.embed([text])
        return embeddings[0] if embeddings else []
