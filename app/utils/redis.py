from redis import asyncio as aioredis
from app.utils.config import settings

JTI_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(host=settings.redis_host, port=settings.redis_port, db=0)

async def add_jti_to_blocklist(jti:str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)
    
async def token_in_blocklist(jti:str) -> bool:
    jti = await token_blocklist.get(jti)
    
    return jti is not None