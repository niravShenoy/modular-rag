from fastapi import Depends, APIRouter, HTTPException, UploadFile
from typing import List
from src.api.dependencies import get_config
from src.core.config import Config
from src.rag.ingestion import IngestionService

router = APIRouter(tags=["ingestion"])

@router.post("/ingest")
async def ingest_data(files: List[UploadFile], config: Config = Depends(get_config)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided for ingestion.")
    try:
        # Placeholder for actual ingestion logic
        ingestion_service = IngestionService(config)
        ingestion_service.ingest_data(files)
        return {"status": "Ingested data", "file_count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=F"Ingestion error: {str(e)}")