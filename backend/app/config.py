from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    dashscope_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    chroma_persist_dir: str = "./data/chroma"
    upload_dir: str = "./data/uploads"
    llm_model: str = "qwen3-max"
    available_models: list[str] = ["qwen3-max", "qwen-plus", "qwen-turbo", "qwen-vl-plus"]
    embedding_model: str = "text-embedding-v3"
    chunk_size: int = 800
    chunk_overlap: int = 150
    retrieval_top_k: int = 5
    memory_top_k: int = 3

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
