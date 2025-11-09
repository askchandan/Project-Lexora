"""
Logger utility module
"""

import logging
import os
from typing import Optional


def get_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger instance that writes to a log file.
    
    Args:
        name: Logger name
        level: Logging level
    
    Returns:
        logging.Logger: Configured logger writing to logs/app.log
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create file handler
        log_file = os.path.join(log_dir, "app.log")
        handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        
        # Set formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    
    return logger
