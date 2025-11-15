from fastapi import APIRouter, Depends
from src.api.dependencies import get_config
from src.core.config import Config
from src.models.schemas import ChatRequest, ChatResponse
from src.rag.retriever import RetrieverService

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, config: Config = Depends(get_config)):
    retriever_service = RetrieverService(config)
    documents = retriever_service.get_response(request.query, history=request.history)

    answer = ""
    sources = []
    return ChatResponse(response=answer, sources=sources)