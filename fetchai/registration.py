"""
Agent registration with Agentverse v2 API.

With uagents-core 0.4.0+:
- Registrations are permanent (no 48-hour expiration)
- Agentverse automatically handles Almanac sync
- No separate Almanac registration needed
"""

from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig
from uagents_core.contrib.protocols.chat import chat_protocol_spec
from uagents_core.identity import Identity
from uagents_core.registration import AgentverseConnectRequest
from uagents_core.types import (
    AgentType,
    AgentGeolocation,
    AgentGeoLocationDetails,
)
from uagents_core.utils.registration import (
    register_in_agentverse,
    AgentverseRegistrationRequest,
)

from fetchai.logger import get_logger

logger = get_logger(__name__)


def register_with_agentverse(
    identity: Identity,
    url: str,
    agentverse_token: str,
    agent_title: str,
    readme: str,
    geo_location: AgentGeolocation | AgentGeoLocationDetails | None = None,
    metadata: dict[str, str | list[str] | dict[str, str]] | None = None,
    avatar_url: str | None = None,
    *,
    protocol_digest: str = chat_protocol_spec.digest,
    agent_type: AgentType = "custom",
    is_public: bool = True,
    agentverse_base_url: str = DEFAULT_AGENTVERSE_URL,
) -> bool:
    """
    Register the agent with Agentverse v2 API.

    With v2 API:
    - Registration is permanent (no expiration)
    - Agentverse automatically syncs to Almanac
    - No separate Almanac registration needed

    :param identity: The identity of the agent.
    :param url: The URL endpoint for the agent
    :param agentverse_token: The token to use to authenticate with the Agentverse API
    :param agent_title: The title of the agent
    :param readme: The readme for the agent
    :param geo_location: The location of the agent
    :param metadata: Additional data related to the agent.
    :param avatar_url: The URL of the agent's avatar.
    :param protocol_digest: The digest of the protocol that the agent supports
    :param agent_type: The type of agent (e.g., "custom", "proxy")
    :param is_public: Denotes if the agent should be retrieved by Agentverse search by default.
    :param agentverse_base_url: The base url of the Agentverse environment we would like to use.
    :return: True if registration was successful, False otherwise.
    """
    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    # Build metadata with is_public and geolocation
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
        metadata["geolocation"] = {
            key: str(value)
            for key, value in geo_location.model_dump(exclude_none=True).items()
        }

    # Always use the caller-provided URL as the endpoint.
    # Previously, this function unconditionally overwrote the URL with
    # agentverse_config.proxy_endpoint for agent_type="proxy", which
    # prevented callers from registering their own webhook callback URL.
    # The caller is responsible for passing the correct endpoint URL.

    # Build agent registration request
    agent_details = AgentverseRegistrationRequest(
        name=agent_title,
        endpoint=url,
        protocols=[protocol_digest],
        metadata=metadata,
        type=agent_type,
        description="",  # Short description - can be enhanced later
        readme=readme,
        avatar_url=avatar_url,
    )

    # Connect request with authentication
    connect_request = AgentverseConnectRequest(
        user_token=agentverse_token,
        agent_type=agent_type,
        endpoint=url,
    )

    # Register with Agentverse v2 API
    # This automatically handles Almanac sync - no separate registration needed
    success = register_in_agentverse(
        request=connect_request,
        identity=identity,
        agent_details=agent_details,
        agentverse_config=agentverse_config,
    )

    if not success:
        logger.warning("Failed to register agent in Agentverse")

    return bool(success)
