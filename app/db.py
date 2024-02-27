from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

#TODO Disable echo in production
engine = create_async_engine(settings.db_url, echo=True)
AsyncSessionFactory = async_sessionmaker(engine) #, autoflush=False can be used to avoid refreshing data after each query

Base = declarative_base()

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