"""
LLM factory module for creating language models
"""

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_llm_model(
    model_name: str = "mistralai/mistral-7b-instruct",
    temperature: float = 0.7,
    max_tokens: int = 500
) -> ChatOpenAI:
    """
    Get or create an LLM instance.
    
    Args:
        model_name: Model identifier
        temperature: Creativity parameter (0-1)
        max_tokens: Maximum response length
    
    Returns:
        ChatOpenAI: Configured LLM instance
    """
    model = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv('OPENAI_API_BASE')
    )
    return model
