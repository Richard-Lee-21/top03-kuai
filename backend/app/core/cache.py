import asyncio
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global redis client
redis_client = None

async def init_cache():
    """
    Initialize Redis cache connection
    """
    global redis_client
    
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,  # Automatically decode byte responses to strings
            encoding="utf-8",
        )
        
        # Test connection
        await redis_client.ping()
        logger.info("Redis cache initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Redis cache: {e}")
        raise

def get_redis_client():
    """
    Get Redis client instance
    """
    global redis_client
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call init_cache() first.")
    return redis_client