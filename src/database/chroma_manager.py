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
        
        # Ensure documents are persisted
        try:
            if hasattr(self.db, 'persist'):
                self.db.persist()
                logger.info(f"Persisted {len(documents)} documents to Chroma")
        except Exception as e:
            logger.warning(f"Could not explicitly persist: {e}")
        
        # Verify they were added
        count = self.get_document_count()
        logger.info(f"Added {len(documents)} documents to Chroma (total now: {count})")
    
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
        import time
        import gc
        
        logger.info("START delete_all()")
        logger.info(f"Persist directory: {self.persist_directory}")
        logger.info(f"Directory exists before delete: {os.path.exists(self.persist_directory)}")
        
        try:
            # Force garbage collection
            logger.info("Closing connections...")
            gc.collect()
            
            # Close the current database connection thoroughly
            if hasattr(self.db, '_client'):
                self.db._client = None
            if hasattr(self.db, 'db'):
                self.db.db = None
            self.db = None
            
            # Wait for file handles to release
            time.sleep(2)
            gc.collect()
            logger.info("Connections closed, waiting for file handles...")
        except Exception as e:
            logger.warning(f"Could not close connection: {e}")
        
        # Delete the directory with retries
        retry_count = 0
        max_retries = 3
        
        logger.info(f"Attempting to delete {self.persist_directory}...")
        while retry_count < max_retries and os.path.exists(self.persist_directory):
            try:
                logger.info(f"Delete attempt {retry_count + 1}/{max_retries}...")
                shutil.rmtree(self.persist_directory)
                logger.info(f"Successfully deleted {self.persist_directory}")
                break
            except Exception as e:
                retry_count += 1
                logger.warning(f"Attempt {retry_count} to delete failed: {e}")
                time.sleep(0.5)
                
                if retry_count >= max_retries:
                    # Last resort: try Windows rmdir command
                    import subprocess
                    try:
                        logger.info("Trying Windows rmdir command...")
                        subprocess.run(['rmdir', '/s', '/q', self.persist_directory], 
                                     shell=True, check=False, timeout=5)
                        logger.info("Deleted via Windows rmdir command")
                    except Exception as e2:
                        logger.error(f"Could not delete directory: {e2}")
                        raise
        
        logger.info(f"Directory exists after delete attempt: {os.path.exists(self.persist_directory)}")
        
        # Recreate fresh database
        logger.info("Recreating fresh database...")
        gc.collect()
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        logger.info(f"Fresh database created. Directory exists: {os.path.exists(self.persist_directory)}")
        logger.info(f"Document count in fresh DB: {self.get_document_count()}")
        logger.info("END delete_all()")
    
    def get_document_count(self) -> int:
        """Get the number of documents in the database"""
        items = self.db.get(include=[])
        return len(items.get("ids", []))
