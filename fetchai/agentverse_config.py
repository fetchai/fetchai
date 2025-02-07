from typing import Literal
from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig


AgentverseEnv = Literal["prod", "canary", "staging"]


def create_agentverse_config(env: AgentverseEnv) -> AgentverseConfig:
    """
    Create a config to point to a specific Almanac+Agentverse environment
        so that non-prod Almanac+Agentverse environments can be used too (for testing).
    :param env: The environment we would like to use - can be prod/canary/staging.
    :return: The AgentverseConfig object containing the url corresponding to the specific env.
    """

    agentverse_subdomain = "" if env == "prod" else env
    agentverse_base_url = (
        f"{agentverse_subdomain}.{DEFAULT_AGENTVERSE_URL}"
        if agentverse_subdomain
        else DEFAULT_AGENTVERSE_URL
    )
    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    return agentverse_config
