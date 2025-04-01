from fastapi import FastAPI
from .routers import users


app = FastAPI()

app.include_router(router=users.router)


@app.get("/api/v1/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to THE BEAUTIFUL CHURCH API", "version NO.": 1.0}
