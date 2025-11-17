from fastapi import Depends, Request
from src.core.config import Config
from src.rag.vector_store import VectorStoreService

def get_config() -> Config:
    return Config()

def get_vector_store(request: Request) -> VectorStoreService:
    return request.app.state.vector_store