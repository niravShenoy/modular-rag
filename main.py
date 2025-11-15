import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from src.api.routers.ingestion_router import IngestionRouter
from src.api.routers.chat_router import ChatRouter
from src.api.routers.config_router import ConfigRouter

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG API", version="1.0.0")

# app.include_router(IngestionRouter(), prefix="/v1")
# app.include_router(ChatRouter(), prefix="/v1")
# app.include_router(ConfigRouter(), prefix="/v1")


@app.get("/")
def main():
    return {"message": "Welcome to the RAG API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
