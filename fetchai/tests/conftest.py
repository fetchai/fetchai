import json
import os

import pytest
from agentverse_client.search import AgentSearchResponse


@pytest.fixture
def agent_search_response_fixture() -> dict:
    json_file_path = os.path.join(os.path.dirname(__file__), "test_agent.json")

    with open(json_file_path, "r", encoding="utf-8") as f:
        return AgentSearchResponse.model_validate(json.load(f)).model_dump()
