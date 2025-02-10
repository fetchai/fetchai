from typing import Optional

import agentverse_client.search
from agentverse_client.search import (
    AgentSearchResponse,
    AgentFilters,
    SortType,
    Direction,
)


class AIEngine:
    configuration: agentverse_client.search.Configuration

    def __init__(self, url: str = "https://agentverse.ai"):
        self.configuration = agentverse_client.search.Configuration(host=url)

    def search_agent(
        self,
        query: str,
        protocol: Optional[
            str
        ] = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    ) -> AgentSearchResponse:
        with agentverse_client.search.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = agentverse_client.search.SearchApi(api_client)
            agent_search_request = agentverse_client.search.AgentSearchRequest(
                search_text=query,
                filters=AgentFilters(protocol_digest=[protocol]),
                sort=SortType.RELEVANCY,
                direction=Direction.ASC,
                offset=0,
                limit=10,
            )

            try:
                # Search Agents
                api_response: AgentSearchResponse = api_instance.search_agents(
                    agent_search_request
                )
                return api_response
            except Exception as e:
                print("Exception when calling SearchApi->search_agents: %s\n" % e)
                raise
