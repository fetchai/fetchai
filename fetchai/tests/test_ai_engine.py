from unittest import mock

from fetchai.ai_engine import AIEngine


class TestAIEngineIntegration:
    ai_engine: AIEngine

    @classmethod
    def setup_class(cls):
        cls.ai_engine = AIEngine()

    def test_search_agents(self):
        with mock.patch(
            "agentverse_client.search.SearchApi.search_agents"
        ) as search_agents_mock:
            ai_engine = AIEngine()
            ai_engine.search_agent(query="Find me a restaurant.")
            assert search_agents_mock.call_count == 1
