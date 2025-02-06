from typing import Optional
from urllib.parse import urlparse
from uagents_core.config import AgentverseConfig
from uagents_core.crypto import Identity
from uagents_core.registration import AgentverseConnectRequest, AgentUpdates
from uagents_core.types import AgentType
from uagents_core.utils.registration import register_in_almanac, register_in_agentverse


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    *,
    protocol_digest: str = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    almanac_api: Optional[str] = None,
    agent_type: AgentType = "custom",
):
    """
    Register the agent with the Agentverse API.
    :param identity: The identity of the agent.
    :param url: The URL endpoint for the agent
    :param agentverse_token: The token to use to authenticate with the Agentverse API
    :param agent_title: The title of the agent
    :param readme: The readme for the agent
    :param protocol_digest: The digest of the protocol that the agent supports
    :param almanac_api: The URL of the Almanac API (if different from the default)
    :return:
    """

    # Create config for Almanac registration (by register_in_almanac method)
    # This config will not be used for Agentverse registration (by register_in_agentverse method)
    # TODO: Doesn't make sense to me to make only the Almanac registration configurable (by almanac_api arg)
    #   but not the Agentverse registration
    #   but that's how this method was implemented before so I will stick to that implementation
    if almanac_api:
        almanac_api_parsed = urlparse(almanac_api)
        protocol = almanac_api_parsed.scheme
        base_url = f"{almanac_api_parsed.netloc}{almanac_api_parsed.path}"

        almanac_config = AgentverseConfig(
            base_url=base_url, protocol=protocol, http_prefix=protocol
        )
    else:
        # use production Agentverse for Almanac registration
        almanac_config = AgentverseConfig()

    agentverse_connect_request = AgentverseConnectRequest(
        user_token=agentverse_token,
        agent_type=agent_type,
        endpoint=url,
    )

    register_in_almanac(
        request=agentverse_connect_request,
        identity=identity,
        protocol_digests=[protocol_digest],
        agentverse_config=almanac_config,
    )

    agent_updates = AgentUpdates(name=agent_title, readme=readme)
    register_in_agentverse(
        request=agentverse_connect_request,
        identity=identity,
        agent_details=agent_updates,
        # Agentverse registration is not configurable (<-> Almanac registration (register_in_almanac method))
        #   = it always uses production Agentverse
        agentverse_config=AgentverseConfig(),
    )
