"""
Decorators for ICT Trading AI Agent
"""

import time
import functools
import logging
from typing import Any, Callable, Optional
import asyncio
from cachetools import TTLCache
import hashlib
import json

logger = logging.getLogger(__name__)

# Global cache for decorators
_cache = TTLCache(maxsize=1000, ttl=300)

def monitor_performance(func: Callable) -> Callable:
    """Monitor function performance"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    return wrapper

def monitor_performance_async(func: Callable) -> Callable:
    """Monitor async function performance"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Retry decorator with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {e}")
            
            raise last_exception
        return wrapper
    return decorator

def retry_async(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Async retry decorator with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"{func.__name__} attempt {attempt + 1} failed: {e}. Retrying in {current_delay}s")
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {e}")
            
            raise last_exception
        return wrapper
    return decorator

def cache_result(ttl_seconds: int = 300):
    """Cache function results"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key from function name and arguments
            cache_data = {
                'func': func.__name__,
                'args': str(args),
                'kwargs': str(sorted(kwargs.items()))
            }
            cache_key = hashlib.md5(json.dumps(cache_data, sort_keys=True).encode()).hexdigest()
            
            # Check cache
            if cache_key in _cache:
                logger.debug(f"Cache hit for {func.__name__}")
                return _cache[cache_key]
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            _cache[cache_key] = result
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        return wrapper
    return decorator

def validate_data(required_columns: Optional[list] = None, min_rows: int = 1):
    """Validate DataFrame input"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Find DataFrame in arguments
            df = None
            for arg in args:
                if hasattr(arg, 'columns') and hasattr(arg, 'index'):
                    df = arg
                    break
            
            if df is None:
                for value in kwargs.values():
                    if hasattr(value, 'columns') and hasattr(value, 'index'):
                        df = value
                        break
            
            if df is not None:
                # Validate DataFrame
                if len(df) < min_rows:
                    raise ValueError(f"DataFrame has {len(df)} rows, need at least {min_rows}")
                
                if required_columns:
                    missing_cols = [col for col in required_columns if col not in df.columns]
                    if missing_cols:
                        raise ValueError(f"Missing required columns: {missing_cols}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator