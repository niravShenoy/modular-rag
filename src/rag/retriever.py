from typing import List, Dict, Any
import os
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import numpy as np

from src.core.config import Config
from src.rag.vector_store import VectorStoreService as VectorStore
from src.rag.embedding import EmbeddingService

class RetrieverService:
    def __init__(self, vector_store: VectorStore, config: Config, top_k: int = 5):
        """
        Initialize the RAG Retriever.
        """
        if vector_store is None:
            self.vector_store = VectorStoreService(config)
        else:
            self.vector_store = vector_store
        self.embedding_model = EmbeddingService(model_name=config.model_name)
        self.config = config
        self.top_k = top_k

    def retrieve_documents(self, query: str, top_k: int = None, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for the given query.

        Args:
            query (str): The input query string.
            score_threshold (float): Minimum similarity score to consider a document relevant.
        Returns:
            List[Dict[str, Any]]: List of retrieved documents with metadata and similarity scores.
        """
        top_k = top_k if top_k is not None else self.top_k
        try:
            query_embedding = self.embedding_model.embed_chunks([query])[0]
            results = self.vector_store.collection.query(
                query_embeddings=query_embedding,
                n_results=top_k,
            )

            retrieved_docs = []
            doc_count = 0

            if results and 'documents' in results and len(results['documents']) > 0:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]

                for i, (doc, metadata, distance, doc_id) in enumerate(zip(documents, metadatas, distances, ids)):
                    similarity_score = 1 / (1 + distance)  # Convert distance to similarity score

                    if similarity_score >= score_threshold:
                        doc_count += 1
                        retrieved_docs.append({
                            "document": doc,
                            "metadata": metadata,
                            "similarity_score": similarity_score,
                            "distance": distance,
                            "id": doc_id
                        })

                print(f"Retrieved {doc_count} documents above the score threshold of {score_threshold}.")

            return retrieved_docs

        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
        
    def rag_simple(self, query: str, llm: Any, top_k: int = 3) -> str:
        results = self.retrieve_documents(query, top_k=top_k)
        context="\n\n".join([doc['document'] for doc in results]) if results else ""
        if not context:
            return "No relevant context found to answer the question."

        prompt=f"""Use the following context to answer the question concisely with precision.
                Context: 
                {context}

                Question: 
                {query}

                Answer:"""
        
        response = llm.invoke([prompt.format(context=context, query=query)])
        return response.content
    
    def rag_advanced(self, query: str, llm: Any, top_k: int = 5, min_score: float = 0.2, return_context: bool = False) -> Dict[str, Any]:
        """
        RAG pipeline with extra features:
        - minimum similarity score filtering
        - returns confidence score
        - option to return context/source along with answer
        """
        results = self.retrieve_documents(query, top_k=top_k, score_threshold=min_score)
        if not results:
            return {
                    'answer': 'No relevant context found.',
                    'sources': [],
                    'confidence_score': 0.0,
                    'context': ''
                }
        
        context = "\n\n".join([doc['document'] for doc in results])
        sources =[{
            'source': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
            'page': doc['metadata'].get('page', 'unknown'),
            'score': doc['similarity_score'],
            'preview': doc['document'][:200] + '...'
        } for doc in results]

        confidence = np.max([doc['similarity_score'] for doc in results])

        prompt = f"""Use the following context to answer the question concisely with precision. If the answer is not found in the context, respond with 'Information not available in the provided context.'.
                Context: 
                {context}

                Question: 
                {query}

                Answer:"""
        
        response = llm.invoke([prompt.format(context=context, query=query)])

        output = {
            'answer': response.content,
            'sources': sources,
            'confidence_score': confidence,
            'context': context if return_context else None
        }

        return output

        
    def get_response(self, query: str, history: List[Dict[str, Any]] = None) -> str:
        """
        Generate a response for the given query using retrieved documents.

        Args:
            query (str): The input query string.
            history (List[Dict[str, Any]], optional): Conversation history for context.
            
        Returns:
            str: The generated response.
        """
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")

            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables.")

            # 1. Initialize ChatGroq LLM
            chat_groq = ChatOllama(
                            model="llama3.2:latest",
                            temperature=0.2,
                            num_predict=1000
                        )
            
            # 2. Retrieve relevant documents
            if self.config.retrieval_strategy == "simple":
                response = self.rag_simple(query, llm=chat_groq, top_k=self.top_k)
            
            elif self.config.retrieval_strategy == "advanced":
                response = self.rag_advanced(query, llm=chat_groq, top_k=self.top_k, min_score=0.2, return_context=True)
            else:
                raise ValueError(f"Unsupported retrieval strategy: {self.config.retrieval_strategy}")
            
            return response
        
        except Exception as e:
            raise ValueError(f"Error generating response: {e}")

    