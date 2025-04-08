from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig
from uagents_core.identity import Identity
from uagents_core.registration import AgentUpdates, AgentverseConnectRequest
from uagents_core.types import AgentType
from uagents_core.utils.registration import register_in_agentverse, register_in_almanac
from uagents_core.contrib.protocols.chat import chat_protocol_spec

from fetchai.schema import AgentGeoLocation


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    geo_location: AgentGeoLocation | None = None,
    *,
    protocol_digest: str = chat_protocol_spec.digest,
    agent_type: AgentType = "custom",
    agentverse_base_url: str = DEFAULT_AGENTVERSE_URL,
) -> None:
    """
    Register the agent with the Agentverse API.
    :param identity: The identity of the agent.
    :param url: The URL endpoint for the agent
    :param protocol_digest: The digest of the protocol that the agent supports
    :param agentverse_token: The token to use to authenticate with the Agentverse API
    :param agent_title: The title of the agent
    :param readme: The readme for the agent
    :param geo_location: The location of the agent
    :param agentverse_base_url: The base url of the Agentverse environment we would like to use.
    :return:
    """

    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    almanac_url = url
    if agent_type == "proxy":
        almanac_url = agentverse_config.proxy_endpoint

    register_in_almanac(
        identity=identity,
        endpoints=[almanac_url],
        protocol_digests=[protocol_digest],
        metadata={"geolocation": geo_location.as_str_dict()} if geo_location else None,
        agentverse_config=agentverse_config,
    )

    register_in_agentverse(
        request=AgentverseConnectRequest(
            user_token=agentverse_token,
            agent_type=agent_type,
            endpoint=url,
        ),
        identity=identity,
        agent_details=AgentUpdates(
            name=agent_title,
            readme=readme,
        ),
        agentverse_config=agentverse_config,
    )
