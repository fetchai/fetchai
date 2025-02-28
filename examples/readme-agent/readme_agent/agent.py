from fastapi import FastAPI

from fetchai.communication import (
    parse_message_from_agent_message_dict,
)
from fetchai.schema import EncodedAgentMessage

app = FastAPI()


@app.get("/")
async def healthcheck():
    return


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
    return
