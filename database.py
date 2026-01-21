## database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
# . is the current directory

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# sqllite generally allows only one thread, but fastapi handles multiple requests across threads - you wouldn't need to do this for postgres of mysql

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# sessionlocal = factory that creates a database session
# sesssion = transaction with the database, each request gets its own session
# we want to control when the changes are committed, that's why autoflush=False, autocommit=False.




class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db
# the dependency function that provides sessions to our routes,
# this is a generator using this yeild db
# with statement makes the session works like a context manager. kind of like opening a file
# this ensures clean=up evenif an error occurs
# fastapi's dependency injection calls this function for each requests handles that handles the clean up automatically


# dependency injection -> this route needs a database session to work so go ahead and give it one.
# instead of creating the session inside the route.

