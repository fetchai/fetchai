import os
import sys

import click


# Load environment variables from .env and validate keys
def load_environment_variables():
    agentverse_key = os.getenv("AGENTVERSE_KEY")
    agent_key = os.getenv("AGENT_KEY")

    if not agentverse_key or not agent_key:
        click.echo(
            "Error: AGENTVERSE_KEY or AGENT_KEY not found in environment variables."
        )
        sys.exit(1)

    return agentverse_key, agent_key
