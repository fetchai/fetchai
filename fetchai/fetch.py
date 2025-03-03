from typing import Optional, Callable, TypeVar, Any

import agentverse_client.search
from agentverse_client.search import (
    AgentSearchResponse,
    SearchApi,
    AgentFilters,
    Direction,
    SortType,
)
from agentverse_client.search.models.search_feedback_request import (
    SearchFeedbackRequest,
)
from pydantic import BaseModel


def ai(
    query: str,
    protocol: Optional[
        str
    ] = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
) -> dict:
    agent_search_request = agentverse_client.search.AgentSearchRequest(
        search_text=query,
        filters=AgentFilters(protocol_digest=[protocol]),
        sort=SortType.RELEVANCY,
        direction=Direction.ASC,  # TODO: Should not be this DESC?
        offset=0,
        limit=10,
    )

    req: Callable[[SearchApi], AgentSearchResponse] = (
        lambda api_instance: api_instance.search_agents(agent_search_request)
    )

    try:
        api_response: AgentSearchResponse = _request(req)
        result: dict = api_response.model_dump()
        result["ais"] = result.get("agents", [])
        return result
    except Exception as e:
        print("Exception when calling SearchApi->search_agents: %s\n" % e)
        return {"ais": [], "error": f"{e}"}


T = TypeVar("T", bound=BaseModel)


def _request(request: Callable[[SearchApi], T]) -> T:
    url = "https://agentverse.ai"
    configuration = agentverse_client.search.Configuration(host=url)
    with agentverse_client.search.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance: SearchApi = agentverse_client.search.SearchApi(api_client)
        return request(api_instance)


def feedback(search_response: dict, agent_index: int) -> None:
    page_index: int = search_response.get("offset") // search_response.get("num_hits")
    search_feedback_request = SearchFeedbackRequest(
        search_id=search_response.get("search_id"),
        page_index=page_index,
        address=search_response.get("agents")[agent_index].get("address"),
    )

    req: Callable[[SearchApi], Any] = lambda api_instance: api_instance.feedback(
        search_feedback_request
    )

    try:
        _request(req)
    except Exception as e:
        print("Exception when calling SearchApi->search_agents: %s\n" % e)
        raise
