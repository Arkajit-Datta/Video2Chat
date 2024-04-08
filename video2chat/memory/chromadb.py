import os
import uuid
from dotenv import load_dotenv
from typing import Any, Optional, Iterable, List

import chromadb
from chromadb import Settings
from chromadb.utils import embedding_functions

from video2chat.memory.base import VectorStore
from video2chat.memory.document import Document
from video2chat.memory.embedding.base import BaseEmbedding

load_dotenv()

def _build_chroma_client():
    chroma_host_name = "localhost"
    chroma_port = 8000
    return chromadb.Client(Settings(chroma_api_impl="rest", chroma_server_host=chroma_host_name,
                                    chroma_server_http_port=chroma_port))


class ChromaDB(VectorStore):
    def __init__(
            self,
            collection_name: str,
            embedding_model: BaseEmbedding,
            text_field: str,
            namespace: Optional[str] = "",
    ):
        self.client = _build_chroma_client()
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.text_field = text_field
        self.namespace = namespace
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
    @classmethod
    def create_collection(cls, collection_name):
        """Create a Chroma Collection.
        Args:
        collection_name: The name of the collection to create.
        """
        chroma_client = _build_chroma_client()
        return chroma_client.get_or_create_collection(name=collection_name, embedding_function=cls.add_embeddings_to_vector_db)

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

        metadatas = []
        ids = ids or [str(uuid.uuid4()) for _ in texts]
        if len(ids) < len(texts):
            raise ValueError("Number of ids must match number of texts.")

        for text, id in zip(texts, ids):
            metadata = metadatas.pop(0) if metadatas else {}
            metadata[self.text_field] = text
            metadatas.append(metadata)
        collection = self.client.get_collection(name=self.collection_name)
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        return ids

    def get_matching_text(self, query: str, top_k: int = 5, metadata: Optional[dict] = {}, **kwargs: Any) -> List[
        Document]:
        """Return docs most similar to query using specified search type."""
        embedding_vector = self.embedding_model.get_embedding(query)
        collection = self.client.get_collection(name=self.collection_name)
        filters = {}
        for key in metadata.keys():
            filters[key] = metadata[key]
        results = collection.query(
            query_embeddings=embedding_vector,
            include=["documents"],
            n_results=top_k,
            where=filters
        )

        documents = []

        for node_id, text, metadata in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0]):
            documents.append(
                Document(
                    text_content=text,
                    metadata=metadata
                )
            )

        return documents

    def get_index_stats(self) -> dict:
        pass

    def add_embeddings_to_vector_db(self, embedding_func_name: str = "text-embedding-ada-002"):
        embedding_func = embedding_functions.OpenAIEmbeddingFunction(
            api_key=self.openai_key,
            model_name=embedding_func_name,
        )
        return embedding_func

    def delete_embeddings_from_vector_db(self, ids: List[str]) -> None:
        pass