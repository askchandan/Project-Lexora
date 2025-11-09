#!/usr/bin/env python
"""
Query Script
Execute queries against the RAG system
"""

import argparse
import sys
import os

# Add parent directory to path to allow imports from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.query_engine import QueryEngine
from src.utils import load_config, get_logger

logger = get_logger(__name__)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Query the RAG system for legal information"
    )
    parser.add_argument(
        "query",
        type=str,
        help="The question to ask the system"
    )
    parser.add_argument(
        "-k",
        "--top-k",
        type=int,
        default=5,
        help="Number of relevant documents to retrieve (default: 5)"
    )
    
    args = parser.parse_args()
    config = load_config()
    
    try:
        # Initialize query engine
        engine = QueryEngine(
            chroma_path=config['chroma_path'],
            model_name=config.get('model_name', 'mistralai/mistral-7b-instruct')
        )
        
        # Execute query
        answer, sources = engine.query(args.query, top_k=args.top_k)
        
        # Display results
        print("\n" + "=" * 70)
        print("RESPONSE")
        print("=" * 70)
        print(answer)
        print("\n" + "-" * 70)
        print("SOURCES")
        print("-" * 70)
        for source in sources:
            print(f"  - {source}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
