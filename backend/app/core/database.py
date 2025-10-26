import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.configuration import Base
import logging

logger = logging.getLogger(__name__)

# Global variables for database connections
engine = None
AsyncSessionLocal = None

async def init_db():
    """
    Initialize database connection and create tables
    """
    global engine, AsyncSessionLocal
    
    from app.core.config import settings
    
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,  # Set to True for debugging
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    
    # Create async session factory
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database initialized successfully")

async def get_db() -> AsyncSession:
    """
    Get database session dependency for FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_engine():
    """
    Get sync engine for Alembic migrations
    """
    from app.core.config import settings
    return create_engine(
        settings.DATABASE_URL.replace("asyncpg", "psycopg2"),
        echo=False,
    )