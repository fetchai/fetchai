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
        "sender":"agent1q2rkmh7a7fka48mf5rp9pt37n2fccppvwlcfjtlpeankh02nhae0vy7nffs",
        "target":"agent1q2rkmh7a7fka48mf5rp9pt37n2fccppvwlcfjtlpeankh02nhae0vy7nffs",
        "session":"c26e5ba8-d2c8-49ae-bf42-dd8636d5f6fa",
        "schema_digest":"model:708d789bb90924328daa69a47f7a8f3483980f16a1142c24b12972a2e4174bc6",
        "protocol_digest":"proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2",
        "payload":"eyJxdWVzdGlvbiI6IkJ1eSBtZSBhIHBhaXIgb2Ygc2hvZXMiLCJzaG9lX3NpemUiOjEyLCJmYXZvcml0ZV9jb2xvciI6ImJsYWNrIn0=",
        "expires":null,
        "nonce":null,
        "signature":"sig1yc6sw6eumnjx0lyyvkgn2wyffwk5jleg4lvqvkfjc9we3ee7js9wz2vlrad9terj4zx55mq3rm60ea7jnlwl5tavge04x5p52knd7hqg90lkv"
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



@app.post("/webhook")
async def webhook(agent_message: EncodedAgentMessage):
    print("Webhook called")
    print(agent_message)

    message = parse_message_from_agent_message_dict(agent_message.model_dump(by_alias=True))

    print(message)

    return {"status": "OK So far!"}

    # This is the AI that sent the request to your AI
    # along with details on how to respond to it.
    # sender = message.sender

    # This is the request that the sender AI sent your
    # AI. Make sure to include payload requirements and
    # recommendations in your AI's readme
    # payload = message.payload

    # Assuming the sending AI included your required parameters
    # you can access the question we identified as a requirement
    # message = payload.get("question", "")
    # print(f"Have your AI process the message {message}")

    # Send a response if needed to the AI that asked
    # for help
    # ai_identity = Identity.from_seed(os.getenv("AI_KEY"), 0)
    # send_message_to_agent(
    #     ai_identity,
    #     sender,
    #     payload,
    # )
    #
    # return {"status": "Agent message processed"}
