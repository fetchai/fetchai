import os

from dotenv import load_dotenv
from uagents_core.identity import Identity

load_dotenv()


# Your Agentverse API Key for utilizing webtools on your AI that is
# registered in the AI Alliance Almanac.
AGENTVERSE_KEY = os.getenv("AGENTVERSE_KEY")

# The local url your agent is running at
MY_WEBHOOK_URL = os.getenv("MY_WEBHOOK_URL")

# A nice name for your agent
MY_AGENT_NAME = os.getenv("MY_AGENT_NAME")

# A unique seed to use for your Identity creation - do not use the
# defaults.
MY_AI_KEY = os.getenv("MY_AI_KEY")

if "Generate a unique string" in MY_AI_KEY:
    raise ValueError(
        "Do not use the default value for MY_AI_KEY - Generate a unique string in your .env file"
    )

# The Identity to use for your agent
AGENT_IDENTITY = Identity.from_seed(MY_AI_KEY, 0)

# Used for extracting those pieces of information from an agent readme
# that are actually relevant when searching agents based on a short search text.
ASI1_URL = "https://api.asi1.ai/v1"
ASI1_API_KEY = os.getenv("ASI1_API_KEY")
ASI1_MODEL_NAME = os.getenv("ASI1_MODEL_NAME", "asi1-mini")
