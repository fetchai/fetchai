import os

from dotenv import load_dotenv
from fetchai import fetch
from fetchai.crypto import Identity
from fetchai.communication import send_message_to_agent


load_dotenv()

AGENT_ADDRESS = "<Add the Agentverse Address of your registered agent here>"
MY_AI_KEY = os.getenv("MY_AI_KEY")


def main():
    query = "Buy me a pair of shoes"

    # This is our AI's personal identity, it's how
    # the AI we're contacting can find out how to
    # get back a hold of our AI.
    # This must match the Identity created when your agent was registered
    sender_identity = Identity.from_seed(os.getenv("MY_AI_KEY"), 0)

    # We'll make up a payload here, but you should
    # use the readme provided by the other AIs to have
    # your AI dynamically create the payload.
    payload = {
        "question": "Buy me a pair of shoes",
        "shoe_size": 12,
        "favorite_color": "black",
    }

    # Send your message and include your AI's identity
    # to enable dialogue between your AI and the
    # one you are sending the request to.
    send_message_to_agent(
        sender_identity,
        AGENT_ADDRESS,
        payload,
    )


if __name__ == "__main__":
    main()
