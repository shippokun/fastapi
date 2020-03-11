from starlette.testclient import TestClient
from app.main import app
from app.db import session

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
