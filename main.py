import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from src.core.config import Config
from src.rag.vector_store import VectorStoreService
from src.api.routers.ingestion_router import router as ingestion_router
from src.api.routers.chat_router import router as chat_router
from src.api.routers.config_router import router as config_router

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()
vector_store = VectorStoreService(config)

@asynccontextmanager
async def lifespan(app):
    # attach vector_store to app.state so it is available to routes and can be saved on shutdown
    app.state.vector_store = vector_store
    try:
        yield
    finally:
        if hasattr(app.state, 'vector_store') and hasattr(app.state.vector_store, 'save'):
            app.state.vector_store.save()  # e.g., for FAISS/Chroma

app = FastAPI(title="RAG API", version="1.0.0", lifespan=lifespan)

app.include_router(ingestion_router, prefix="/v1")
app.include_router(chat_router, prefix="/v1")
app.include_router(config_router, prefix="/v1")


@app.get("/")
def main():
    return {"message": "Welcome to the RAG API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
