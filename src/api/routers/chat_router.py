from fastapi import APIRouter, Depends

from src.rag.vector_store import VectorStoreService
from src.api.dependencies import get_config, get_vector_store
from src.core.config import Config
from src.models.schemas import ChatRequest, ChatResponse
from src.rag.retriever import RetrieverService

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, vector_store: VectorStoreService = Depends(get_vector_store), config: Config = Depends(get_config)):
    retriever_service = RetrieverService(vector_store, config)
    documents = retriever_service.get_response(request.query, history=request.history)

    if config.retrieval_strategy == "advanced":
        answer = documents['answer']
        sources = documents['sources']
    elif config.retrieval_strategy == "simple":
        answer = documents['answer']
        sources = []

    return ChatResponse(response=answer, sources=sources)