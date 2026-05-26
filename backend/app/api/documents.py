import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.config import settings
from app.models.orm import Document
from app.models.schemas import DocumentOut, UploadResponse
from app.services.parser import DocumentParser, detect_file_type
from app.services.chunker import TextChunker
from app.services.embeddings import EmbeddingService
from app.services.vector_store import vector_store
from app.services.llm import ImageDescriber

router = APIRouter()


@router.post("/documents/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file_type = detect_file_type(file.filename)
    if file_type == "unknown":
        raise HTTPException(400, f"Unsupported file type: {file.filename}")

    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(settings.upload_dir, safe_name)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    document = Document(
        filename=file.filename,
        file_type=file_type,
        file_path=file_path,
        status="processing",
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    try:
        text = DocumentParser.parse(file_path, file_type)

        if file_type == "pdf":
            images = DocumentParser.extract_images_from_pdf(file_path)
            describer = ImageDescriber()
            descriptions = []
            for img in images[:5]:
                desc = describer.describe_image(img)
                if desc and "非图表" not in desc:
                    descriptions.append(desc)
            if descriptions:
                text += "\n\n## 图表描述\n" + "\n".join(descriptions)

        chunker = TextChunker()
        chunks = chunker.split(text)

        embedding_service = EmbeddingService()
        chunk_embeddings = embedding_service.embed(chunks)

        emb_dim = len(chunk_embeddings[0]) if chunk_embeddings else 1024
        collection_name = vector_store.create_collection(document.id, emb_dim)
        vector_store.add_chunks(collection_name, chunks, chunk_embeddings)

        document.chunk_count = len(chunks)
        document.status = "ready"
    except Exception as e:
        document.status = "error"
        await db.commit()
        raise HTTPException(500, f"Processing error: {str(e)}")

    await db.commit()

    return UploadResponse(
        id=document.id,
        filename=document.filename,
        file_type=document.file_type,
        status=document.status,
        message=f"Processed {len(chunks)} chunks",
    )


@router.get("/documents", response_model=list[DocumentOut])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).order_by(Document.created_at.desc())
    )
    return result.scalars().all()


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(404, "Document not found")

    vector_store.delete_collection(doc_id)

    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    await db.delete(doc)
    await db.commit()
    return {"status": "deleted"}
