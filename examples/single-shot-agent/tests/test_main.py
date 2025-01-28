from fastapi.testclient import TestClient

from single_shot_agent.main import app

client = TestClient(app)


def test_root_url_200():
    response = client.get("/")

    assert response.status_code == 200
