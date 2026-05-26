import os
import json
import numpy as np
import faiss
from typing import List, Optional
from app.config import settings


class VectorStore:
    """FAISS vector store for document chunks."""

    def __init__(self):
        self.base_dir = settings.chroma_persist_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _index_path(self, doc_id: int) -> str:
        return os.path.join(self.base_dir, f"doc_{doc_id}.index")

    def _chunks_path(self, doc_id: int) -> str:
        return os.path.join(self.base_dir, f"doc_{doc_id}.chunks.json")

    def create_collection(self, doc_id: int, embedding_dim: int) -> str:
        index = faiss.IndexIDMap(faiss.IndexFlatIP(embedding_dim))
        faiss.write_index(index, self._index_path(doc_id))
        return f"doc_{doc_id}"

    def add_chunks(
        self,
        collection_name: str,
        chunks: List[str],
        embeddings: List[List[float]],
    ) -> None:
        doc_id = int(collection_name.split("_")[1])
        index_path = self._index_path(doc_id)
        chunks_path = self._chunks_path(doc_id)

        index = faiss.read_index(index_path)

        vectors = np.array(embeddings).astype(np.float32)
        # Normalize for cosine similarity (inner product on normalized = cosine)
        faiss.normalize_L2(vectors)

        n = index.ntotal
        ids = np.array([n + i for i in range(len(chunks))]).astype(np.int64)
        index.add_with_ids(vectors, ids)

        faiss.write_index(index, index_path)

        existing = []
        if os.path.exists(chunks_path):
            with open(chunks_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(chunks)
        with open(chunks_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False)

    def search(
        self,
        collection_names: List[str],
        query_embedding: List[float],
        top_k: int = None,
    ) -> List[str]:
        if not collection_names:
            return []

        top_k = top_k or settings.retrieval_top_k
        all_chunks = []

        for name in collection_names:
            doc_id = int(name.split("_")[1])
            index_path = self._index_path(doc_id)
            chunks_path = self._chunks_path(doc_id)

            if not os.path.exists(index_path) or not os.path.exists(chunks_path):
                continue

            index = faiss.read_index(index_path)
            if index.ntotal == 0:
                continue

            with open(chunks_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

            vec = np.array([query_embedding]).astype(np.float32)
            faiss.normalize_L2(vec)

            k = min(top_k, index.ntotal)
            distances, indices = index.search(vec, k)

            for idx in indices[0]:
                if 0 <= idx < len(chunks):
                    all_chunks.append(chunks[int(idx)])

        return all_chunks

    def delete_collection(self, doc_id: int) -> None:
        index_path = self._index_path(doc_id)
        chunks_path = self._chunks_path(doc_id)
        for p in [index_path, chunks_path]:
            if os.path.exists(p):
                os.remove(p)

    def _memory_index_path(self) -> str:
        return os.path.join(self.base_dir, "memory.index")

    def _memory_chunks_path(self) -> str:
        return os.path.join(self.base_dir, "memory.chunks.json")

    def get_or_create_memory_collection(self) -> str:
        idx_path = self._memory_index_path()
        chunks_path = self._memory_chunks_path()
        if not os.path.exists(idx_path):
            emb_dim = 1024
            index = faiss.IndexIDMap(faiss.IndexFlatIP(emb_dim))
            faiss.write_index(index, idx_path)
        if not os.path.exists(chunks_path):
            with open(chunks_path, "w", encoding="utf-8") as f:
                json.dump([], f)
        return "conversation_memory"

    def add_memory(
        self,
        summary: str,
        embedding: List[float],
        meta_id: str,
    ) -> None:
        self.get_or_create_memory_collection()
        idx_path = self._memory_index_path()
        chunks_path = self._memory_chunks_path()

        index = faiss.read_index(idx_path)
        vec = np.array([embedding]).astype(np.float32)
        faiss.normalize_L2(vec)
        n = index.ntotal
        ids = np.array([n]).astype(np.int64)
        index.add_with_ids(vec, ids)
        faiss.write_index(index, idx_path)

        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        chunks.append(summary)
        with open(chunks_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False)

    def search_memory(
        self,
        query_embedding: List[float],
        top_k: int = None,
    ) -> List[str]:
        top_k = top_k or settings.memory_top_k
        idx_path = self._memory_index_path()
        chunks_path = self._memory_chunks_path()

        if not os.path.exists(idx_path):
            return []

        index = faiss.read_index(idx_path)
        if index.ntotal == 0:
            return []

        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        vec = np.array([query_embedding]).astype(np.float32)
        faiss.normalize_L2(vec)

        k = min(top_k, index.ntotal)
        distances, indices = index.search(vec, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(chunks):
                results.append(chunks[int(idx)])
        return results


vector_store = VectorStore()
