import json
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.orm import Conversation, Message, Document
from app.models.schemas import ChatRequest
from app.services.llm import LLMService
from app.services.rag import RAGService

router = APIRouter()


@router.post("/chat/{conv_id}/stream")
async def chat_stream(
    conv_id: int,
    body: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    conv = await db.get(Conversation, conv_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    user_msg = Message(conversation_id=conv_id, role="user", content=body.query)
    db.add(user_msg)
    await db.commit()

    history = await _get_chat_history(db, conv_id)
    doc_ids = await _get_document_ids(db)

    async def event_generator():
        rag = RAGService()
        context = ""

        if doc_ids:
            doc_chunks = rag.retrieve_documents(body.query, doc_ids)
            memories = rag.retrieve_memories(body.query)
            context = rag.build_context(doc_chunks, memories)

        system_prompt = rag.build_system_prompt(context)

        llm = LLMService()
        full_response = ""

        yield f"data: {json.dumps({'type': 'start', 'context_length': len(context)}, ensure_ascii=False)}\n\n"

        async for token in llm.generate_stream(system_prompt, history):
            full_response += token
            yield f"data: {json.dumps({'type': 'token', 'content': token}, ensure_ascii=False)}\n\n"

        yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

        assistant_msg = Message(
            conversation_id=conv_id, role="assistant", content=full_response
        )
        db.add(assistant_msg)

        conv.title = body.query[:50]
        await db.commit()

        summary_prompt = f"用户: {body.query}\n助手: {full_response}"
        summary = await llm.summarize(summary_prompt)
        if summary:
            memory_id = f"conv_{conv_id}_{uuid.uuid4().hex[:8]}"
            rag.store_memory(summary, memory_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


async def _get_chat_history(db: AsyncSession, conv_id: int) -> List[dict]:
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conv_id)
        .order_by(Message.created_at.asc())
        .limit(20)
    )
    messages = result.scalars().all()
    return [{"role": m.role, "content": m.content} for m in messages]


async def _get_document_ids(db: AsyncSession) -> List[int]:
    result = await db.execute(
        select(Document.id).where(Document.status == "ready")
    )
    return [row[0] for row in result.fetchall()]
