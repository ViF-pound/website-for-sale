from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import config

engine = create_async_engine(url = config.env_data.db_url_async, echo=True)

assync_session = sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with assync_session() as session:
        yield session

class Base(DeclarativeBase):
    ...