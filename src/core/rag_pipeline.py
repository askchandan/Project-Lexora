"""
RAG Pipeline - Retrieval-Augmented Generation
"""

from typing import List, Tuple, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from src.database.chroma_manager import ChromaManager
from src.utils import get_logger

logger = get_logger(__name__)


class RAGPipeline:
    """Manages the complete RAG pipeline"""
    
    def __init__(self, data_path: str, chroma_path: str):
        """
        Initialize RAG pipeline.
        
        Args:
            data_path: Path to PDF data directory
            chroma_path: Path to Chroma database
        """
        self.data_path = data_path
        self.vector_store = ChromaManager(chroma_path)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        logger.info(f"Initialized RAG Pipeline with data from {data_path}")
    
    def load_documents(self) -> List[Document]:
        """Load documents from PDF directory"""
        logger.info(f"Loading documents from {self.data_path}")
        loader = PyPDFDirectoryLoader(self.data_path)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        logger.info("Splitting documents into chunks")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        return chunks
    
    def add_chunks_to_database(self, chunks: List[Document]) -> int:
        """Add document chunks to vector database"""
        # Calculate chunk IDs
        chunks_with_ids = self._calculate_chunk_ids(chunks)
        logger.info(f"Calculated IDs for {len(chunks_with_ids)} chunks")
        
        # Get existing documents
        existing_count = self.vector_store.get_document_count()
        logger.info(f"Found {existing_count} existing documents in database")
        
        # Add new documents
        existing_items = self.vector_store.db.get(include=[])
        existing_ids = set(existing_items.get("ids", []))
        logger.info(f"Found {len(existing_ids)} existing IDs in database")
        
        new_chunks = [
            chunk for chunk in chunks_with_ids
            if chunk.metadata.get("id") not in existing_ids
        ]
        
        logger.info(f"Found {len(new_chunks)} new chunks to add")
        
        if new_chunks:
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            logger.info(f"Adding {len(new_chunks)} chunks with IDs: {new_chunk_ids[:3]}...")
            
            self.vector_store.add_documents(new_chunks, ids=new_chunk_ids)
            
            # Verify they were added
            final_count = self.vector_store.get_document_count()
            logger.info(f"Added {len(new_chunks)} new documents. Final count: {final_count}")
            
            if final_count > existing_count:
                logger.info(f"✓ Success! Database grew from {existing_count} to {final_count}")
            else:
                logger.warning(f"⚠ Warning: Added {len(new_chunks)} chunks but count didn't change ({existing_count} -> {final_count})")
            
            return len(new_chunks)
        else:
            logger.info("No new documents to add (all already in database)")
            return 0
    
    def _calculate_chunk_ids(self, chunks: List[Document]) -> List[Document]:
        """Calculate unique IDs for chunks"""
        last_page_id = None
        current_chunk_index = 0
        
        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"
            
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0
            
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            chunk.metadata["id"] = chunk_id
            last_page_id = current_page_id
        
        return chunks
    
    def clear_database(self) -> None:
        """Clear the entire database"""
        logger.warning("Clearing database")
        self.vector_store.delete_all()
