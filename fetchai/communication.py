import json
from typing import Optional, Any
from uuid import uuid4

from pydantic import UUID4
from uagents_core.config import AgentverseConfig
from uagents_core.crypto import Identity
from uagents_core.envelope import Envelope
from uagents_core.utils.communication import send_message

from fetchai.schema import JsonStr, AgentMessage


def send_message_to_agent(
    sender: Identity,
    target: str,
    payload: Any,
    session: Optional[UUID4] = uuid4(),
    # The default protocol for AI to AI conversation, use for standard chat
    protocol_digest: Optional[
        str
    ] = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    # The default model for AI to AI conversation, use for standard chat
    model_digest: Optional[
        str
    ] = "model:708d789bb90924328daa69a47f7a8f3483980f16a1142c24b12972a2e4174bc6",
    agentverse_base_url: str = "agentverse.ai",
):
    """
    Send a message to an agent.
    :param session: The unique identifier for the dialogue between two agents
    :param sender: The identity of the sender.
    :param target: The address of the target agent.
    :param protocol_digest: The digest of the protocol that is being used
    :param model_digest: The digest of the model that is being used
    :param payload: The payload of the message.
    :param env: The Agentverse environment we would like to use - default is prod.
    :return:
    """

    agentverse_config = AgentverseConfig(base_url=agentverse_base_url)

    send_message(
        destination=target,
        message_schema_digest=model_digest,
        message_body=payload,
        sender=sender,
        session_id=session,
        protocol_digest=protocol_digest,
        agentverse_config=agentverse_config,
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
