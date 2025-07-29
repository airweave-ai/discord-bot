import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    decode_responses=True,
    db=0
)