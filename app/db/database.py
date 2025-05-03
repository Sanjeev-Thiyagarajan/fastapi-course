from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from app.utils.config import settings
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    url=settings.database_url,
    echo=True,
    connect_args = {"statement_cache_size":0}
)




async def initdb():
    """Create a connection to our DB"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()-> AsyncSession:
    "Create session for user"
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session





































