from typing import List, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, SentenceTransformersTokenTextSplitter

from src.core.config import Config


class ChunkingService:
    def __init__(self, config: Config, chunk_size: int = 1000, chunk_overlap: int = 200, retrieval_strategy: str = "recursive"):
        self.chunk_size = config.chunk_size
        self.chunk_overlap = config.chunk_overlap
        self.chunking_strategy = config.chunking_strategy

    def chunk_documents(self, documents: List[Any], **kwargs: Any,) -> List[Any]:
        """
        Chunk documents into smaller pieces based on chunk_size and chunk_overlap.

        Args:
            documents (List[Any]): List of documents to be chunked.
            **kwargs: Additional keyword arguments.

        Returns:
            List[Any]: List of chunked documents.
        """
        documents_chunks = []

        if self.chunking_strategy == "recursive":
            length_function = kwargs.get("length_function", len)
            is_separator_regex = kwargs.get("is_separator_regex", False)

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=length_function,
                is_separator_regex=is_separator_regex,
            )
            for document in documents:
                chunks = text_splitter.split_documents([document])
                documents_chunks.extend(chunks)
            return documents_chunks
        
        elif self.chunking_strategy == "sentence_transformers":
            model_name = kwargs.get("model_name", "all-MiniLM-L6-v2")

            try:
                text_splitter = SentenceTransformersTokenTextSplitter(
                    model_name=model_name,
                    chunk_overlap=self.chunk_overlap,
                )

                for document in documents:
                    chunks = text_splitter.split_documents([document])
                    documents_chunks.extend(chunks)

                return documents_chunks
            except Exception as e:
                raise ValueError(f"Error initializing SentenceTransformersTokenTextSplitter: {e}")
        
        elif self.chunking_strategy == "character":
            model_name = kwargs.get("model_name", "gpt-4")

            text_splitter = CharacterTextSplitter(
                model_name=model_name,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
            )

            for document in documents:
                chunks = text_splitter.split_documents([document])
                documents_chunks.extend(chunks)

            return documents_chunks
        
        else:
            raise ValueError(f"Unsupported chunking strategy: {self.chunking_strategy}")