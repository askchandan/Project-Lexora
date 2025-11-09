"""
Chroma vector database manager
"""

import os
import shutil
from typing import List, Tuple, Any
from langchain_chroma import Chroma
from src.database.vector_store import VectorStore
from src.models import get_embedding_function
from src.utils import get_logger

logger = get_logger(__name__)


class ChromaManager(VectorStore):
    """Manages Chroma vector database operations"""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize Chroma manager.
        
        Args:
            persist_directory: Path to persist the database
        """
        self.persist_directory = persist_directory
        self.embedding_function = get_embedding_function()
        self.db = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_function
        )
        logger.info(f"Initialized Chroma at {persist_directory}")
    
    def add_documents(self, documents: List[Any], ids: List[str]) -> None:
        """
        Add documents to Chroma database.
        
        Args:
            documents: List of documents to add
            ids: Unique IDs for each document
        """
        self.db.add_documents(documents, ids=ids)
        logger.info(f"Added {len(documents)} documents to Chroma")
    
    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[Any, float]]:
        """
        Search for similar documents.
        
        Args:
            query: Query text
            k: Number of results to return
        
        Returns:
            List of (document, score) tuples
        """
        results = self.db.similarity_search_with_score(query, k=k)
        logger.info(f"Found {len(results)} similar documents for query")
        return results
    
    def delete_all(self) -> None:
        """Delete all documents and reset the database"""
        try:
            # Close the current database connection
            if hasattr(self.db, '_client'):
                self.db._client = None
            
            # Wait a moment for file handles to release
            import time
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Could not close connection: {e}")
        
        # Delete the directory
        if os.path.exists(self.persist_directory):
            try:
                shutil.rmtree(self.persist_directory)
                logger.info(f"Deleted Chroma database at {self.persist_directory}")
            except Exception as e:
                logger.warning(f"Could not delete directory: {e}")
                # Try force remove on Windows
                import subprocess
                try:
                    subprocess.run(['rmdir', '/s', '/q', self.persist_directory], 
                                 shell=True, check=False)
                except:
                    pass
        
        # Recreate fresh database
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        logger.info("Initialized fresh Chroma database")
    
    def get_document_count(self) -> int:
        """Get the number of documents in the database"""
        items = self.db.get(include=[])
        return len(items.get("ids", []))
