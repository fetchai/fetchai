from typing import Optional

from fastapi import FastAPI, Request

from fetchai.communication import (
    parse_message_from_agent,
    parse_message_from_agent_message_dict,
    send_message_to_agent,
)
from pydantic import BaseModel, Field


app = FastAPI()


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


@app.get("/")
async def healthcheck():
    return {"Status": "OK"}


@app.post("/webhook")
async def webhook(agent_message: EncodedAgentMessage):
    """Simple webhook to receive messages for this agent"""

    # For now, just print everything out
    print("Webhook called")
    print(agent_message)

    message = parse_message_from_agent_message_dict(
        agent_message.model_dump(by_alias=True)
    )
    print(message)

    # TODO - implement your response to the message here

    return {"status": "OK So far!"}
