from pydantic import BaseModel
import yaml
from pathlib import Path
from typing import Dict, Any

class Config(BaseModel):
    embedding_provider: str = "huggingface"
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store_provider: str = "chroma"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    chunking_strategy: str = "recursive"
    top_k: int = 5
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    persist_directory: str = "./data/vector_store"
    collection_name: str = "default_collection"
    retrieval_strategy: str = "advanced"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_defaults()

    def load_defaults(self):
        config_path = Path(__file__).parent.parent / "config" / "default.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                defaults = yaml.safe_load(f)
                for key, value in defaults.items():
                    if not hasattr(self, key) or getattr(self, key) is None:
                        setattr(self, key, value)

    def update_config(self, updates: Dict[str, Any]):
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid config key: {key}")