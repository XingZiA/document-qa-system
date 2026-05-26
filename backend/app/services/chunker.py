import re
from typing import List

from app.config import settings


class TextChunker:
    """Split text into overlapping chunks for embedding."""

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []

        separators = ["\n\n", "\n", ". ", "。 ", " ", ""]
        for sep in separators:
            if sep:
                parts = text.split(sep)
            else:
                parts = [text]

            chunks = []
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if len(part) <= self.chunk_size:
                    chunks.append(part)
                else:
                    for i in range(0, len(part), self.chunk_size - self.chunk_overlap):
                        chunk = part[i:i + self.chunk_size]
                        if chunk.strip():
                            chunks.append(chunk.strip())

            if chunks:
                break

        chunks = self._merge_short_chunks(chunks)
        return chunks

    def _merge_short_chunks(self, chunks: List[str]) -> List[str]:
        merged = []
        buffer = ""
        for chunk in chunks:
            if len(buffer) + len(chunk) <= self.chunk_size:
                buffer = (buffer + " " + chunk).strip() if buffer else chunk
            else:
                if buffer:
                    merged.append(buffer)
                buffer = chunk
        if buffer:
            merged.append(buffer)
        return merged
