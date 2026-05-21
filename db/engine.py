import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/monitoring_db"
)


engine = create_async_engine(DB_URL, echo=False)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db(metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    print("[SYSTEM] Database tables synchronized successfully.")