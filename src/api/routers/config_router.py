from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_config
from src.core.config import Config
from src.models.schemas import ConfigUpdate

router = APIRouter(tags=["config"])

@router.post("/config")
async def update_config(update: ConfigUpdate, config: Config = Depends(get_config)):
    """
    Update configuration settings.
    """
    try:
        config.update_config(update.updates)
        return {"status": "update", "current_config": config.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))