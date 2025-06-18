from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig
from uagents_core.contrib.protocols.chat import chat_protocol_spec
from uagents_core.identity import Identity
from uagents_core.registration import AgentUpdates, AgentverseConnectRequest
from uagents_core.types import AgentType
from uagents_core.utils.registration import register_in_agentverse, register_in_almanac

from fetchai.logger import get_logger
from fetchai.schema import AgentGeoLocation

logger = get_logger(__name__)


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    geo_location: AgentGeoLocation | None = None,
    metadata: dict[str, str | list[str] | dict[str, str]] | None = None,
    *,
    protocol_digest: str = chat_protocol_spec.digest,
    agent_type: AgentType = "custom",
    is_public: bool = True,
    agentverse_base_url: str = DEFAULT_AGENTVERSE_URL,
) -> bool:
    """
    Register the agent with the Agentverse API.
    :param identity: The identity of the agent.
    :param url: The URL endpoint for the agent
    :param protocol_digest: The digest of the protocol that the agent supports
    :param agentverse_token: The token to use to authenticate with the Agentverse API
    :param agent_title: The title of the agent
    :param readme: The readme for the agent
    :param metadata: Additional data related to the agent.
    :param geo_location: The location of the agent
    :param is_public: Denotes if the agent should be retrieved by Agentverse search by default.
    :param agentverse_base_url: The base url of the Agentverse environment we would like to use.
    :return: True if registration was successful in both Almanac and Agentverse, False otherwise.
    """

    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    almanac_url = url
    if agent_type == "proxy":
        almanac_url = agentverse_config.proxy_endpoint

    metadata = metadata or {}
    if "is_public" in metadata:
        logger.warning(
            "The value of metadata belonging to key 'is_public' will be overwritten by `is_public` arg"
        )
    metadata["is_public"] = str(is_public)
    if geo_location:
        if "geolocation" in metadata:
            logger.warning(
                "The value of metadata belonging to key 'geolocation' will be overwritten by `geo_location` arg"
            )
        metadata["geolocation"] = geo_location.as_str_dict()

    register_in_almanac_success = register_in_almanac(
        identity=identity,
        endpoints=[almanac_url],
        protocol_digests=[protocol_digest],
        metadata=metadata,
        agentverse_config=agentverse_config,
    )

    if not register_in_almanac_success:
        logger.warning("Failed to register agent in Almanac")
        return False

    register_in_agentverse_success = register_in_agentverse(
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

    if not register_in_agentverse_success:
        logger.warning("Failed to register agent in Agentverse")

    return bool(register_in_agentverse_success and register_in_almanac_success)
