from typing import Optional

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


def ai(
    query: str,
    protocol: Optional[
        str
    ] = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
) -> dict:
    res: dict = {"ais": []}

    agent_search_request = agentverse_client.search.AgentSearchRequest(
        search_text=query,
        filters=AgentFilters(protocol_digest=[protocol]),
        sort=SortType.RELEVANCY,
        direction=Direction.ASC,  # ! Right now, in the API, ASC & DESC are reversed
        offset=0,
        limit=10,
    )

    try:
        with agentverse_client.search.ApiClient() as api_client:
            api_instance: SearchApi = agentverse_client.search.SearchApi(api_client)
            api_response: AgentSearchResponse = api_instance.search_agents(
                agent_search_request
            )

        api_response_dict: dict = api_response.model_dump()

        res["ais"] = api_response_dict.get("agents", [])
        res["search_id"] = api_response_dict["search_id"]
        res["offset"] = api_response_dict["offset"]
        res["num_hits"] = api_response_dict["num_hits"]

        return res
    except Exception as e:
        print("Exception when calling SearchApi->search_agents: %s\n" % e)
        return {"ais": [], "error": f"{e}"}


def feedback(search_response: dict, agent_index: int) -> None:
    page_index: int = search_response.get("offset") // search_response.get("num_hits")
    search_feedback_request = SearchFeedbackRequest(
        search_id=search_response.get("search_id"),
        page_index=page_index,
        address=search_response.get("ais")[agent_index].get("address"),
    )

    try:
        with agentverse_client.search.ApiClient() as api_client:
            api_instance: SearchApi = agentverse_client.search.SearchApi(api_client)
            api_instance.feedback(search_feedback_request)
    except Exception as e:
        print("Exception when calling SearchApi->feedback: %s\n" % e)
        raise
