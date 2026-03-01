## database.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"
# . is the current directory

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# sqllite generally allows only one thread, but fastapi handles multiple requests across threads - you wouldn't need to do this for postgres of mysql

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False # prevents issue with expired objects after a commit.
)
# sessionlocal = factory that creates a database session
# sesssion = transaction with the database, each request gets its own session
# we want to control when the changes are committed, that's why autoflush=False, autocommit=False.

# expire_on_commit - when an object expired sqlalchemy would normally try to reload it lazily
# but lazy loading doesn't work in async


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
# the dependency function that provides sessions to our routes,
# this is a generator using this yeild db
# with statement makes the session works like a context manager. kind of like opening a file
# this ensures clean=up evenif an error occurs
# fastapi's dependency injection calls this function for each requests handles that handles the clean up automatically


# dependency injection -> this route needs a database session to work so go ahead and give it one.
# instead of creating the session inside the route.

