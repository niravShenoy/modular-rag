from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from langchain_openai import OpenAIEmbeddings

from src.core.config import Config

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        """
        self.model_name = model_name
        self.model = None
        self.model = self._load_model(config=Config())

    def _load_model(self, config: Config) -> Embeddings:
        """
        Load the embedding model.
        """
        try:
            if config.embedding_provider == "openai":
                print(f"Using OpenAI Embeddings with model: {config.model_name}")
                self.model = OpenAIEmbeddings(model=config.model_name)
            elif config.embedding_provider == "huggingface":
                self.model = SentenceTransformer(config.model_name)
            else:
                raise ValueError(f"Unsupported embedding provider: {config.embedding_provider}")
            return self.model
            
        except Exception as e:
            raise ValueError(f"Error loading model {config.model_name}: {e}")

    def embed_chunks(self, chunks: List[str]) -> List[np.ndarray]:
        """
        Embed a list of documents.
        """
        try:
            return self.model.encode(chunks)
        except Exception as e:
            raise ValueError(f"Error embedding documents: {e}")