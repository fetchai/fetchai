from fastapi.testclient import TestClient

from readme_agent.agent import app


client = TestClient(app)


class TestHealthCheckEndpoint:
    def test_healthcheck_at_root_url_returns_200(self):
        response = client.get("/")

        assert response.status_code == 200
