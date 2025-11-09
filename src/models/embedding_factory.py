"""
Embedding factory module for creating embedding functions
"""

from langchain_openai import OpenAIEmbeddings
from typing import Any


def get_embedding_function() -> OpenAIEmbeddings:
    """
    Get or create the embedding function using OpenAI.
    
    Returns:
        OpenAIEmbeddings: Configured embedding function
    """
    embeddings = OpenAIEmbeddings()
    return embeddings
