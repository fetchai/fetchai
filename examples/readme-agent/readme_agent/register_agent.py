import os

from dotenv import load_dotenv

from fetchai.crypto import Identity
from fetchai.registration import register_with_agentverse


load_dotenv()
# Your Agentverse API Key for utilizing webtools on your AI that is
# registered in the AI Alliance Almanac.
AGENTVERSE_KEY = os.getenv("AGENTVERSE_KEY")
MY_AI_KEY = os.getenv("MY_AI_KEY")


def main():
    # Your AI's unique key for generating an address on agentverse
    ai_identity = Identity.from_seed(MY_AI_KEY, 0)
    print("Got ai identity")

    # Give your AI a name on agentverse. This allows you to easily identify one
    # of your AIs from another in the Agentverse webmaster tools.
    name = "SimonTestFetchAIOne"

    # This is how you optimize your AI's search engine performance
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

    # The webhook that your AI receives messages on.
    ai_webhook = "https://simon.rowland.ngrok.dev/webhook"

    print("registering with agentverse")
    result = register_with_agentverse(
        ai_identity,
        ai_webhook,
        AGENTVERSE_KEY,
        name,
        readme,
    )

    print("Registration result: ", result)


if __name__ == "__main__":
    main()
