from fastapi import FastAPI
from .models.user import Base
from .routers import users
from .db.database import engine

app = FastAPI()


def create_db_tables():
    """
    Create tables if not created
    """
    Base.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    """
    On application startup
    """
    create_db_tables()


app.include_router(router=users.router)


@app.get("/api/v1/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to THE BEAUTIFUL CHURCH API", "version NO.": "1.0"}
