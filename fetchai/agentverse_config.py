from typing import Literal
from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig


AgentverseEnv = Literal["prod", "canary", "staging"]


def create_agentverse_config(env: AgentverseEnv) -> AgentverseConfig:
    """
    Create a config to point to a specific Agentverse environment
        so that non-prod Agentverse environments can be used too (for testing).
    :param env: The environment we would like to use - can be prod/canary/staging.
    :return: The AgentverseConfig object containing the url corresponding to the specific env.
    """

    if env == "prod":
        return AgentverseConfig()

    agentverse_base_url = f"{env}.{DEFAULT_AGENTVERSE_URL}"
    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)
    return agentverse_config
