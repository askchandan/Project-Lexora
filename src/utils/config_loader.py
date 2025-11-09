"""
Configuration loader utility
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables and .env file.
    
    Returns:
        Dict containing all configuration values
    """
    load_dotenv()
    
    config = {
        'data_path': os.getenv('DATA_PATH', 'data'),
        'chroma_path': os.getenv('CHROMA_PATH', 'chroma_db'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'openai_api_base': os.getenv('OPENAI_API_BASE'),
        'model_name': os.getenv('MODEL_NAME', 'mistralai/mistral-7b-instruct'),
        'temperature': float(os.getenv('TEMPERATURE', 0.7)),
        'max_tokens': int(os.getenv('MAX_TOKENS', 500)),
    }
    
    return config
