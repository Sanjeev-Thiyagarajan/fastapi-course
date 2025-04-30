from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from app.utils.config import settings


engine = AsyncEngine(
    create_engine(
        url=settings.database_url,
        echo=True,
        connect_args={"statement_cache_size":0}
    )
)

async def initdb():
    """create a connection with our db"""
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

        
async def get_session() -> AsyncSession:
    "Creates a session for the DB(Dependency to provide to session object)"
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session





# engine = create_engine(settings.database_url)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
