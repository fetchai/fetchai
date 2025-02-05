import base64
import hashlib
import json
import struct
from typing import Optional, Any, Self

from pydantic import BaseModel, Field, UUID4

from fetchai.crypto import Identity


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


class Envelope(BaseModel):
    version: int
    sender: str
    target: str
    session: UUID4
    schema_digest: str
    protocol_digest: Optional[str] = (
        "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
    )
    payload: Optional[str] = None
    expires: Optional[int] = None
    nonce: Optional[int] = None
    signature: Optional[str] = None

    def encode_payload(self, value: JsonStr):
        self.payload = base64.b64encode(value.encode()).decode()

    def decode_payload(self) -> str:
        if self.payload is None:
            return ""

        return base64.b64decode(self.payload).decode()

    def sign(self, identity: Identity):
        try:
            self.signature = identity.sign_digest(self._digest())
        except Exception as err:
            raise ValueError(f"Failed to sign envelope: {err}") from err

    def verify(self) -> bool:
        if self.signature is None:
            raise ValueError("Envelope signature is missing")
        return Identity.verify_digest(self.sender, self._digest(), self.signature)

    def _digest(self) -> bytes:
        hasher = hashlib.sha256()
        hasher.update(self.sender.encode())
        hasher.update(self.target.encode())
        hasher.update(str(self.session).encode())
        hasher.update(self.schema_digest.encode())
        if self.payload is not None:
            hasher.update(self.payload.encode())
        if self.expires is not None:
            hasher.update(struct.pack(">Q", self.expires))
        if self.nonce is not None:
            hasher.update(struct.pack(">Q", self.nonce))
        return hasher.digest()


class AgentMessage(BaseModel):
    # The address of the sender of the message.
    sender: str
    # The address of the target of the message.
    target: str
    # The payload of the message.
    payload: Any

    @classmethod
    def from_envelope(cls, envelope: Envelope) -> Self:
        json_payload = envelope.decode_payload()
        payload = json.loads(json_payload)

        return AgentMessage(
            sender=envelope.sender, target=envelope.target, payload=payload
        )
