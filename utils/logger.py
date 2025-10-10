import functools
import logging
from typing import Callable

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_rating_operations(func: Callable) -> Callable:
    """Декоратор для логирования операций с рейтингом"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        try:
            character_id = kwargs.get('character_id') or (args[1] if len(args) > 1 else None)
            rating = kwargs.get('rating') or (args[2] if len(args) > 2 else None)
            
            logger.info(f"Rating operation: {func.__name__}, character_id: {character_id}, new_rating: {rating}")
            result = await func(*args, **kwargs)
            logger.info(f"Rating operation successful: {func.__name__}, character_id: {character_id}")
            return result
        except Exception as e:
            logger.error(f"Rating operation failed: {func.__name__}, error: {e}")
            raise
    return wrapper