from fetchai.registration import register_with_agentverse
from readme_agent.settings import (
    AGENT_IDENTITY,
    AGENTVERSE_KEY,
    MY_AGENT_NAME,
    MY_WEBHOOK_URL,
)


def main():
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

    print("Registering with agentverse")
    register_with_agentverse(
        AGENT_IDENTITY,
        MY_WEBHOOK_URL,
        AGENTVERSE_KEY,
        MY_AGENT_NAME,
        readme,
    )
    print("Registered agent at:", AGENT_IDENTITY.address)


if __name__ == "__main__":
    main()
