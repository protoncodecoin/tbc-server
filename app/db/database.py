from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


POSTGRES_DATABASE_UL: str = "postgresql://postgres:skyrim@localhost/tbc"


engine = create_engine(POSTGRES_DATABASE_UL, echo=True)

# SessionLocal = sessionmaker(autoflush=False, bind=engine)
