from typing import List, Optional
from app.services.embeddings import EmbeddingService
from app.services.vector_store import vector_store


class RAGService:
    """Orchestrates retrieval-augmented generation."""

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def retrieve_documents(
        self,
        query: str,
        doc_ids: List[int],
        top_k: int = None,
    ) -> List[str]:
        query_embedding = self.embedding_service.embed_single(query)
        collection_names = [f"doc_{did}" for did in doc_ids]
        return vector_store.search(collection_names, query_embedding, top_k)

    def retrieve_memories(self, query: str, top_k: int = None) -> List[str]:
        query_embedding = self.embedding_service.embed_single(query)
        return vector_store.search_memory(query_embedding, top_k)

    def store_memory(self, qa_summary: str, meta_id: str):
        embedding = self.embedding_service.embed_single(qa_summary)
        vector_store.add_memory(qa_summary, embedding, meta_id)

    @staticmethod
    def build_context(
        doc_chunks: List[str],
        memories: List[str],
    ) -> str:
        parts = []
        if memories:
            parts.append("## 历史相关对话\n" + "\n".join(f"- {m}" for m in memories))
        if doc_chunks:
            parts.append("## 参考文档内容\n" + "\n\n---\n".join(doc_chunks))
        return "\n\n".join(parts)

    @staticmethod
    def build_system_prompt(context: str) -> str:
        return f"""你是一个专业的文档问答助手。请根据提供的文档内容回答用户问题。
如果文档中没有相关信息，请如实说明。

回答要求：
- 使用 Markdown 格式，确保列表项、段落之间正确换行
- 每个列表项独占一行（如 1. xxx 后必须换行再接 2. xxx）
- 准确、简洁、有条理

{context}"""
