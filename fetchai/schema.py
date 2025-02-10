import json
from typing import Optional, Any

from pydantic import BaseModel, Field
from uagents_core.envelope import Envelope


class EncodedAgentMessage(BaseModel):
    """
    A Message looks like this on the way in:

    b'{
        "version":1,
        "sender":"<Agentverse Agent Address>",
        "target":"<Agentverse Agent Address>",
        "session":"<Session UUID>",
        "schema_digest":"<Agentverse Schema Digest>",
        "protocol_digest":"<Agentverse Protocol Digest>",
        "payload":"<Encoded Payload>",
        "expires":null,
        "nonce":null,
        "signature":"<Message Signature>"
    }'
    """

    version: int
    sender: str
    target: str
    session: str
    schema_digest: str
    protocol_digest: str
    expires: Optional[str]
    nonce: Optional[str]
    signature: str

    encoded_payload: str = Field(alias="payload")


JsonStr = str


class AgentMessage(BaseModel):
    # The address of the sender of the message.
    sender: str
    # The address of the target of the message.
    target: str
    # The payload of the message.
    payload: Any

    @classmethod
    def from_envelope(cls, envelope: Envelope) -> "AgentMessage":
        json_payload = envelope.decode_payload()
        payload = json.loads(json_payload)

        return AgentMessage(
            sender=envelope.sender, target=envelope.target, payload=payload
        )
