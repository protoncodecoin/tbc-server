from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


POSTGRES_DATABASE_URL: str = "postgresql://postgres:postgres@localhost/tbcDb"

engine = create_engine(POSTGRES_DATABASE_URL, echo=False)


# SessionLocal = sessionmaker(autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass
