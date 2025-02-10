import click
import sys
from dotenv import set_key
from uagents_core.crypto import Identity
from fetchai.registration import register_with_agentverse
from cli.env import load_environment_variables
from cli.readme import load_readme

"""
register.py

This module provides functionality for registering an AI agent with AgentVerse.

The main component of this module is the 'register' command, which is implemented
using the Click library for creating command-line interfaces. This command allows
users to register their AI agent by providing necessary information such as the
AI's name, README file path, and webhook URL.

Usage:
    fetchai-cli register [OPTIONS]

Options:
    -n, --name TEXT     Name of the AI (required, prompted if not provided)
    -r, --readme TEXT   Path to README file (required, prompted if not provided)
    -w, --webhook TEXT  Webhook URL for the AI (required, prompted if not provided)
    -f, --force         Force registration even if agent is already registered
    --help              Show this message and exit.

The registration process includes:
1. Loading environment variables (AgentVerse key and agent key)
2. Reading the content of the provided README file
3. Creating an AI identity using the agent key
4. Registering the agent with AgentVerse
5. Saving the AI identity and name to a .env file

If any errors occur during the registration process, they will be displayed
and the program will exit with a non-zero status code.

Dependencies:
    - click: For creating the command-line interface
    - dotenv: For setting environment variables
    - uagents_core.crypto: For creating AI identity
    - fetchai.registration: For registering with AgentVerse
    - cli.env: For loading environment variables
    - cli.readme: For loading README content

Note: This script assumes that the necessary environment variables (AGENTVERSE_KEY
and AGENT_KEY) are set or can be loaded from a .env file.
"""


# Register command


@click.command(name="register")
@click.option(
    "-n", "--name", prompt="Enter AI name", required=True, help="Name of the AI"
)
@click.option(
    "-r",
    "--readme",
    prompt="Enter README file path",
    required=True,
    help="Path to README file",
)
@click.option(
    "-w",
    "--webhook",
    prompt="Enter Webhook URL",
    required=True,
    help="Webhook URL for the AI",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Force registration even if agent is already registered",
)
def register(name, readme, webhook, force):
    """Register an agent with AgentVerse and save to .env."""
    # Load environment variables and read README file
    agentverse_key, agent_key = load_environment_variables()
    readme_content = load_readme(readme)

    try:
        # Create AI identity
        ai_identity = Identity.from_seed(agent_key, 0)

        # Register the agent with Agentverse
        result = register_with_agentverse(
            ai_identity, webhook, agentverse_key, name, readme_content
        )
        click.echo(f"Agent successfully registered @ {ai_identity.address}")
        # Optionally save information to .env file
        set_key(".env", "AI_IDENTITY", ai_identity.address)
        set_key(".env", "AI_NAME", name)
        click.echo("Identity and name saved to .env.")
    except Exception as e:
        click.echo(f"Error registering agent: {str(e)}")
        sys.exit(1)
