import json
from typing import Any, Optional
from uuid import uuid4

import requests
from pydantic import UUID4
from uagents_core.config import DEFAULT_AGENTVERSE_URL, AgentverseConfig
from uagents_core.envelope import Envelope
from uagents_core.identity import Identity
from uagents_core.types import DeliveryStatus, MsgStatus
from uagents_core.utils.messages import generate_message_envelope, send_message
from uagents_core.utils.resolver import lookup_endpoint_for_agent
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    chat_protocol_spec,
)


from fetchai.schema import AgentMessage, JsonStr


CHAT_MESSAGE_DIGEST = ChatMessage.build_schema_digest(ChatMessage)


def send_message_to_agent(
    sender: Identity,
    target: str,
    payload: Any,
    session: Optional[UUID4] = uuid4(),
    # The default protocol for AI to AI conversation, use for standard chat
    protocol_digest: Optional[
        str
    ] = chat_protocol_spec.digest,
    # The default model for AI to AI conversation, use for standard chat
    model_digest: Optional[
        str
    ] = CHAT_MESSAGE_DIGEST,
    agentverse_base_url: str = DEFAULT_AGENTVERSE_URL,
) -> MsgStatus:
    """
    Send a message to an agent.
    :param session: The unique identifier for the dialogue between two agents
    :param sender: The identity of the sender.
    :param target: The address of the target agent.
    :param protocol_digest: The digest of the protocol that is being used
    :param model_digest: The digest of the model that is being used
    :param payload: The payload of the message.
    :param agentverse_base_url: The base url of the Agentverse environment we would like to use.
    :return:
    """

    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    endpoints: list[str] = lookup_endpoint_for_agent(
        agent_identifier=target, agentverse_config=agentverse_config
    )
    if not endpoints:
        raise ValueError(
            f"Could not find endpoints for agent {target}. Please check the address."
        )

    env: Envelope = generate_message_envelope(
        destination=target,
        message_schema_digest=model_digest,
        message_body=payload,
        sender=sender,
        session_id=session,
        protocol_digest=protocol_digest,
    )

    endpoint = endpoints[0]

    try:
        response = send_message(endpoint, env)
        return MsgStatus(
            status=DeliveryStatus.SENT,
            detail=response.text,
            destination=target,
            endpoint=endpoint,
            session=env.session,
        )
    except requests.RequestException:
        return MsgStatus(
            status=DeliveryStatus.FAILED,
            detail=response.text,
            destination=target,
            endpoint=endpoint,
            session=env.session,
        )


def parse_message_from_agent(content: JsonStr) -> AgentMessage:
    """
    Parse a message from an agent.
    :param content: A string containing the JSON envelope.
    :return: An AgentMessage object.
    """

    env = Envelope.model_validate_json(content)

    if not env.verify():
        raise ValueError("Invalid envelope signature")

    json_payload = env.decode_payload()
    payload = json.loads(json_payload)

    return AgentMessage(sender=env.sender, target=env.target, payload=payload)


def parse_message_from_agent_message_dict(content: dict) -> AgentMessage:
    """
    Parses an agent message from a dict, as typically send to an agent's webhook.
    """

    envelope = Envelope.model_validate(content)

    if not envelope.verify():
        raise ValueError("Invalid Envelope Signature")

    return AgentMessage.from_envelope(envelope)
