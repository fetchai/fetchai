from fetchai.communication import send_message_to_agent
from readme_agent.settings import AGENT_IDENTITY


def main():
    # This is a made up payload
    payload = {
        "question": "Buy me a pair of shoes",
        "shoe_size": 12,
        "favorite_color": "black",
    }

    # Send your message and include your AI's identity
    # to enable dialogue between your AI and the
    # one you are sending the request to.
    send_message_to_agent(
        AGENT_IDENTITY,
        AGENT_IDENTITY.address,
        payload,
    )


if __name__ == "__main__":
    main()
