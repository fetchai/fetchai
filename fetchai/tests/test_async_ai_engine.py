from unittest import mock
from unittest.mock import AsyncMock

import pytest

from fetchai.ai_engine import AsyncAIEngine


class TestAIEngineIntegration:
    ai_engine: AsyncAIEngine

    @classmethod
    def setup_class(cls):
        cls.ai_engine = AsyncAIEngine()

    @pytest.mark.asyncio
    async def test_search_agents(self):
        with mock.patch(
            "agentverse_client.search.aio.SearchApi.search_agents",
            new_callable=AsyncMock,
        ) as search_agents_mock:
            ai_engine = AsyncAIEngine()
            await ai_engine.search_agent(query="Find me a restaurant.")

            assert (
                search_agents_mock.await_count == 1
            ), f"Expected search_agent were awaited once, got {search_agents_mock.call_count} awaits"
