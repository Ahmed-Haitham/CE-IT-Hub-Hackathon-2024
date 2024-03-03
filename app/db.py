from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

#TODO Disable echo in production
engine = create_async_engine(settings.db_url, echo=True)
AsyncSessionFactory = async_sessionmaker(engine, autoflush=False) #, autoflush=False can be used to avoid refreshing data after each query

class Base(DeclarativeBase):
    pass

#This creates the tables in the database
async def start_db(engine):
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

#Functions in main depend on this one to get a session via fastapi's dependency injection
async def get_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()