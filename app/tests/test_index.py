from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..main import app

# app = FastAPI()


# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}


client = TestClient(app)


def test_index():
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to THE BEAUTIFUL CHURCH API",
        "version NO.": "1.0",
    }
