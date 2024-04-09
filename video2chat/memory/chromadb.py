import os
import uuid
import pathlib
from dotenv import load_dotenv
from typing import Any, Optional, Iterable, List

import chromadb
from chromadb import Settings
from chromadb.utils import embedding_functions
from langchain_openai import OpenAIEmbeddings

from video2chat.memory.base import VectorStore
from video2chat.memory.document import Document
from video2chat.memory.embedding.base import BaseEmbedding

load_dotenv()

def _build_chroma_client(chroma_path: str = "video2chat/memory/db/chroma"):
    return chromadb.PersistentClient(chroma_path)


class ChromaDB(VectorStore):
    def __init__(
            self,
            collection_name: str,
            embedding_model: BaseEmbedding,
            text_field: str,
            namespace: Optional[str] = "",
            chroma_path: str = "video2chat/memory/db/chroma",
    ):
        self.client = _build_chroma_client(chroma_path=chroma_path)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.text_field = text_field
        self.namespace = namespace
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
    
    def create_collection(self, collection_name):
        """Create a Chroma Collection.
        Args:
        collection_name: The name of the collection to create.
        """
        chroma_client = _build_chroma_client()
        return chroma_client.get_or_create_collection(name=collection_name, embedding_function=self.add_embeddings_to_vector_db(), metadata={"hnsw:space": "cosine"})

    def add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            ids: Optional[List[str]] = None,
            namespace: Optional[str] = None,
            batch_size: int = 32,
            **kwargs: Any,
    ) -> List[str]:
        """Add texts to the vector store."""
        if namespace is None:
            namespace = self.namespace

        ids = ids or [str(uuid.uuid4()) for _ in texts]
        if len(ids) < len(texts):
            raise ValueError("Number of ids must match number of texts.")

        if metadatas is None:
            metadatas = [{self.text_field: text} for text in texts]
            
        collection = self.client.get_or_create_collection(name=self.collection_name, embedding_function=self.add_embeddings_to_vector_db(), metadata={"hnsw:space": "cosine"})
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        return ids

    def get_matching_text(self, query: str, top_k: int = 5, metadata: Optional[dict] = None, **kwargs: Any) -> List[
        Document]:
        """Return docs most similar to query using specified search type."""
        if metadata is None:
            metadata = {}

        collection = self.client.get_or_create_collection(name=self.collection_name, embedding_function=self.add_embeddings_to_vector_db(), metadata={"hnsw:space": "cosine"})
        filters = {key: metadata[key] for key in metadata.keys()}
        return collection.query(
            query_texts=[query],
            n_results=top_k,
        )

    def get_index_stats(self) -> dict:
        pass

    def add_embeddings_to_vector_db(self, embedding_func_name: str = "text-embedding-ada-002"):
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=self.openai_key,
            model_name=embedding_func_name,
        )

    def delete_embeddings_from_vector_db(self, ids: List[str]) -> None:
        pass