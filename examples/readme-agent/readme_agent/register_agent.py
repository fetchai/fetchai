from fetchai.registration import register_with_agentverse
from fetchai.schema import AgentGeoLocation
from readme_agent.readme_utils import extract_readme
from readme_agent.settings import (
    AGENT_IDENTITY,
    AGENTVERSE_KEY,
    MY_AGENT_NAME,
    MY_WEBHOOK_URL,
)


def main():
    # Use realistic details in your README description to enable discovery of your agent
    readme_metadata = """
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

    readme = extract_readme(readme_metadata)
    geo_location = AgentGeoLocation(latitude=51.169392, longitude=71.449074, radius=0.5)
    metadata = {
        "readme_metadata": readme_metadata,
        "categories": ["business"],
    }

    print("Registering with agentverse")
    success = register_with_agentverse(
        AGENT_IDENTITY,
        MY_WEBHOOK_URL,
        AGENTVERSE_KEY,
        MY_AGENT_NAME,
        readme,
        geo_location,
        metadata,
        is_public=False,
    )
    if success:
        print("Registered agent at:", AGENT_IDENTITY.address)
    else:
        print("Failed to register agent")


if __name__ == "__main__":
    main()
