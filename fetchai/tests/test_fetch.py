from unittest import mock

from fetchai import fetch


class TestAI:
    def test_ai(self):
        with mock.patch(
            "agentverse_client.search.SearchApi.search_agents"
        ) as search_agents_mock:
            fetch.ai(query="Find me a restaurant.")
            assert search_agents_mock.call_count == 1

    def test_feedback(self, agent_search_response_fixture: dict):
        with mock.patch(
            "agentverse_client.search.SearchApi.feedback"
        ) as search_agents_mock:
            fetch.feedback(search_response=agent_search_response_fixture, agent_index=0)
            assert search_agents_mock.call_count == 1
