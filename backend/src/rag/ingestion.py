import os
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from typing import List
from src.core.config import Config

from src.rag.chunking import ChunkingService
from src.rag.embedding import EmbeddingService
from src.rag.vector_store import VectorStoreService


class IngestionService:
    def __init__(self, config: Config, vector_store: VectorStoreService):
        self.config = config
        self.chunking_service = ChunkingService(config)
        if vector_store is None:
            self.vector_store = VectorStoreService(config)
        else:
            self.vector_store = vector_store

    async def ingest_data(self, files: List):
        """
        Document parser service:

        1. Load documents from various file types using langchain loaders.
        
        """
        documents = []
        for file in files:
            content = await file.read()

            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension == ".pdf":
                loader_class = PyMuPDFLoader
            elif file_extension == ".txt":
                loader_class = TextLoader
            
            with tempfile.NamedTemporaryFile(delete=False, suffix="." + file_extension) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            loader = loader_class(temp_file_path)
            docs = loader.load()
            
            os.unlink(temp_file_path)  # Clean up the temporary file
            documents.extend(docs)

        """
        Chunking service

        1. Define chunking service based on config parameters.
        2. Chunk documents into smaller pieces for embedding.        
        
        """
        if not documents:
            raise ValueError("No documents to ingest.")
        
        chunker = ChunkingService(self.config)
        chunks = chunker.chunk_documents(documents)

        """
        Embedding service
        
        1. Initialize embedding model based on config.
        2. Embed document chunks into vector representations.
        """
        embedder = EmbeddingService(model_name=self.config.model_name)

        """
        Vector store service
        
        1. Initialize vector store based on config if not already initialized.
        2. Store embedded vectors into the vector store.
        """

        docs = [chunk.page_content for chunk in chunks]

        # generate embeddings
        embedded_chunks = embedder.embed_chunks(docs)

        # store chunks and embeddings in the vector store
        batch_size = 5461       # max batch size for ChromaDB; add as config later

        # Create batches of chunks and embeddings to avoid memory issues
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            batch_embeddings = embedded_chunks[i:i + batch_size]
            self.vector_store.add_documents(batch_chunks, batch_embeddings)

        print(f"Ingested and stored {len(chunks)} document chunks into the vector store.")
