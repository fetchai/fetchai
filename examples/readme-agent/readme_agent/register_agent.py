import os

from dotenv import load_dotenv

from fetchai.crypto import Identity
from fetchai.registration import register_with_agentverse


load_dotenv()

# Your Agentverse API Key for utilizing webtools on your AI that is
# registered in the AI Alliance Almanac.
AGENTVERSE_KEY = os.getenv("AGENTVERSE_KEY")

# A unique seed to use for your Identity creation - do not use the
# defaults.
MY_AI_KEY = os.getenv("MY_AI_KEY")

# The local url your agent is running at
MY_WEBHOOK_URL = os.getenv("MY_WEBHOOK_URL")

# A nice name for your agent
MY_AGENT_NAME = os.getenv("MY_AGENT_NAME")


if "Generate a unique string" in MY_AI_KEY:
    raise ValueError(
        "Do not use the default value for MY_AI_KEY - Generate a unique string in your .env file"
    )


def main():
    # Your AI's unique key for generating an address on agentverse
    ai_identity = Identity.from_seed(MY_AI_KEY, 0)

    # Use realistic details in your README description to enable discovery of your agent
    readme = """
    <description>My AI's description of capabilities and offerings</description>
    <use_cases>
        <use_case>Answer any single question</use_case>
    </use_cases>
    <payload_requirements>
    <description>None</description>
    <payload>
        <requirement>
            <parameter>question</parameter>
            <description>The question that you would like this AI work with you to solve</description>
        </requirement>
    </payload>
    </payload_requirements>
    """

    print("registering with agentverse")
    result = register_with_agentverse(
        ai_identity,
        MY_WEBHOOK_URL,
        AGENTVERSE_KEY,
        MY_AGENT_NAME,
        readme,
    )
    print("Registration result: ", result)


if __name__ == "__main__":
    main()
