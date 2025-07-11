from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False
)

# Create sessionmaker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get DB session in routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
