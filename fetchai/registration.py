from uagents_core.crypto import Identity
from uagents_core.registration import AgentverseConnectRequest, AgentUpdates
from uagents_core.types import AgentType
from uagents_core.utils.registration import register_in_almanac, register_in_agentverse

from fetchai.agentverse_config import AgentverseEnv, create_agentverse_config


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    *,
    protocol_digest: str = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    agent_type: AgentType = "custom",
    env: AgentverseEnv = "prod",
):
    """
    Register the agent with the Agentverse API.
    :param identity: The identity of the agent.
    :param url: The URL endpoint for the agent
    :param agentverse_token: The token to use to authenticate with the Agentverse API
    :param agent_title: The title of the agent
    :param readme: The readme for the agent
    :param protocol_digest: The digest of the protocol that the agent supports
    :return:
    """

    agentverse_config = create_agentverse_config(env=env)

    agentverse_connect_request = AgentverseConnectRequest(
        user_token=agentverse_token,
        agent_type=agent_type,
        endpoint=url,
    )

    register_in_almanac(
        request=agentverse_connect_request,
        identity=identity,
        protocol_digests=[protocol_digest],
        agentverse_config=agentverse_config,
    )

    agent_updates = AgentUpdates(name=agent_title, readme=readme)
    register_in_agentverse(
        request=agentverse_connect_request,
        identity=identity,
        agent_details=agent_updates,
        agentverse_config=agentverse_config,
    )
