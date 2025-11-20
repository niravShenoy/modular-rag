from typing import List, Any
import uuid
import numpy as np
# from langchain_core.embeddings import Embeddings
import chromadb
import os

from src.core.config import Config

class VectorStoreService:
    def __init__(self, config: Config):
        self.config = config
        self.vector_store_provider = config.vector_store_provider
        self.vector_store = None
        self.embedding_model = config.model_name
        self.persist_directory = config.persist_directory
        self.collection_name = config.collection_name
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """
        Initialize the vector store based on the configuration.
        """
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path = self.persist_directory
            )
            self.collection = self.client.get_or_create_collection(name=self.collection_name)
            print(f"Initialized vector store with collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
        except Exception as e:
            raise ValueError(f"Error initializing vector store: {e}")
        
    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        """
        Add documents and their embeddings to the vector store.

        Args:
            documents (List[Any]): List of documents to add.
            embeddings (np.ndarray): Corresponding embeddings for the documents.
        """
        try:
            if len(documents) != len(embeddings):
                raise ValueError("Number of documents and embeddings must match.")
            
            print(f"Adding {len(documents)} documents to vector store...")
            
            # Prepare data for insertion
            ids = []
            metadatas = []
            document_texts = []
            embeddings_list = []

            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                doc_id = f"doc_{str(uuid.uuid4().hex[:8])}_{i}"
                ids.append(doc_id)

                metadata = dict(doc.metadata)
                metadata['doc_index'] = i
                metadata['content_length'] = len(doc.page_content)
                metadatas.append(metadata)

                document_texts.append(doc.page_content)

                embeddings_list.append(embedding)

            self.collection.add(
                ids=ids,
                metadatas=metadatas,
                documents=document_texts,
                embeddings=embeddings_list
            )
            print("Documents added successfully.")
        except Exception as e:
            raise ValueError(f"Error adding documents to vector store: {e}")