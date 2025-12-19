from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.utils.config import settings


# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True for debugging SQL queries
    pool_pre_ping=True,  # Verify connections before use
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session