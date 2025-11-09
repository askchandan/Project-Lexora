#!/usr/bin/env python
"""
Populate Database Script
Loads PDFs from data directory and populates the Chroma vector database
"""

import argparse
import sys
import os

# Add parent directory to path to allow imports from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.rag_pipeline import RAGPipeline
from src.utils import load_config, get_logger

logger = get_logger(__name__)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Populate Chroma vector database with PDF documents"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset the database before populating"
    )
    
    args = parser.parse_args()
    config = load_config()
    
    try:
        # Initialize RAG pipeline
        pipeline = RAGPipeline(
            data_path=config['data_path'],
            chroma_path=config['chroma_path']
        )
        
        # Reset if requested
        if args.reset:
            logger.info("Resetting database...")
            pipeline.clear_database()
        
        # Load documents
        documents = pipeline.load_documents()
        
        # Split documents
        chunks = pipeline.split_documents(documents)
        
        # Add to database
        added_count = pipeline.add_chunks_to_database(chunks)
        
        logger.info(f"Successfully populated database with {added_count} new documents")
        
    except Exception as e:
        logger.error(f"Error populating database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
