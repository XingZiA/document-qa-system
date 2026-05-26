from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


class ModelSwitchRequest(BaseModel):
    model: str


class SettingsOut(BaseModel):
    llm_model: str
    embedding_model: str
    available_models: list[str]


@router.get("/settings", response_model=SettingsOut)
async def get_settings():
    return SettingsOut(
        llm_model=settings.llm_model,
        embedding_model=settings.embedding_model,
        available_models=settings.available_models,
    )


@router.put("/settings/model")
async def switch_model(body: ModelSwitchRequest):
    if body.model not in settings.available_models:
        raise HTTPException(400, f"Unsupported model: {body.model}. Available: {settings.available_models}")
    settings.llm_model = body.model
    return {"llm_model": settings.llm_model, "message": f"Switched to {body.model}"}
