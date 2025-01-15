from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import get_db_url


engine = create_async_engine(
    get_db_url(),
    echo=True,
    future=True,
)

@asynccontextmanager
async def get_session():
    """
    Контекстный менеджер для работы с БД
    """
    try:
        async_session = sessionmaker(
            engine, class_ = AsyncSession
        )
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
