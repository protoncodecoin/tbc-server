from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from ..schemas.config import settings

DATABASE_URL = settings.DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)


# SessionLocal = sessionmaker(autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass
