from typing import Literal
from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig


AgentverseEnv = Literal["prod", "canary", "staging"]


def create_agentverse_config(env: AgentverseEnv) -> AgentverseConfig:
    agentverse_subdomain = "" if env == "prod" else env
    agentverse_base_url = (
        f"{agentverse_subdomain}.{DEFAULT_AGENTVERSE_URL}"
        if agentverse_subdomain
        else DEFAULT_AGENTVERSE_URL
    )
    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    return agentverse_config
