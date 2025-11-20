from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import UploadFile

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[Dict[str, Any]]] = None

class ConfigUpdate(BaseModel):
    updates: Dict[str, Any]

class IngestionRequest(BaseModel):
    files: List[UploadFile]
    metadata: Optional[Dict[str, Any]] = None