#!/usr/bin/env python
"""
Populate Database Script
Loads PDFs from data directory and populates the Chroma vector database
"""

import argparse
import sys
import os
import shutil
import time

# Add parent directory to path to allow imports from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Delete chroma_db BEFORE importing anything that uses it
def delete_chroma_db(chroma_path: str):
    """Force delete chroma database directory"""
    if os.path.exists(chroma_path):
        try:
            shutil.rmtree(chroma_path)
            print(f"✓ Deleted {chroma_path}")
        except Exception as e:
            print(f"⚠ Warning: Could not delete {chroma_path}: {e}")
            # Try again after a delay
            time.sleep(1)
            try:
                shutil.rmtree(chroma_path)
                print(f"✓ Deleted {chroma_path} on retry")
            except Exception as e2:
                print(f"✗ Failed to delete: {e2}")

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
        help="Reset the database before populating (deletes all existing documents)"
    )
    
    args = parser.parse_args()
    config = load_config()
    
    # Only delete database if explicitly requested with --reset
    if args.reset:
        print("🔄 Resetting database (deleting all existing documents)...")
        delete_chroma_db(config['chroma_path'])
        print("✓ Database reset complete\n")
    else:
        print("📝 Adding new documents (existing documents preserved)...\n")
    
    try:
        # Initialize RAG pipeline (after deletion if needed)
        pipeline = RAGPipeline(
            data_path=config['data_path'],
            chroma_path=config['chroma_path']
        )
        
        # Load documents
        documents = pipeline.load_documents()
        
        # Split documents
        chunks = pipeline.split_documents(documents)
        
        # Add to database (without deleting existing ones)
        added_count = pipeline.add_chunks_to_database(chunks)
        
        if added_count > 0:
            logger.info(f"Successfully added {added_count} new documents")
            print(f"✓ Successfully added {added_count} new documents")
        else:
            logger.info("No new documents to add (all already in database)")
            print(f"ℹ No new documents to add (all already in database)")
        
    except Exception as e:
        logger.error(f"Error populating database: {str(e)}")
        print(f"✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
