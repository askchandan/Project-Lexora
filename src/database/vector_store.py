"""
Vector store abstraction for managing embeddings storage
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Any


class VectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def add_documents(self, documents: List[Any], ids: List[str]) -> None:
        """Add documents to the vector store"""
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[Any, float]]:
        """Search for similar documents"""
        pass
    
    @abstractmethod
    def delete_all(self) -> None:
        """Delete all documents from the store"""
        pass
