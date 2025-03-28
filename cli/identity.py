# cli/identity.py
"""
identity.py

This module provides functionality for generating and managing agent identity keys
within the FetchAI CLI tool. It offers a command-line interface for creating
mnemonic phrases that serve as identity keys for AI agents.

The main component of this module is the 'generate-identity' command, implemented
using the Click library for creating command-line interfaces. This command allows
users to generate a new identity key with specified parameters and optionally save
it to a file or the project's .env file.

Usage:
    fetchai-cli generate-identity [OPTIONS]

Options:
    -s, --strength INTEGER  Strength of the mnemonic (128 or 256 bits) [default: 256]
    -n, --name TEXT         Name of the environment variable [default: AGENT_KEY]
    -o, --output PATH       Output file for saving the generated key
    --help                  Show this message and exit.

The identity generation process includes:
1. Creating a mnemonic phrase using the specified strength
2. Optionally saving the generated key to a specified output file
3. Checking for existing keys in the .env file
4. Prompting for confirmation if overwriting an existing key
5. Saving the new key to the .env file

Key Features:
- Generates mnemonic phrases of either 128 or 256 bits strength
- Allows custom naming of the environment variable for the key
- Provides options for outputting the key to a file or directly to stdout
- Implements safeguards against accidental overwriting of existing keys
- Integrates with the project's .env file for persistent storage of keys

Dependencies:
    - click: For creating the command-line interface
    - dotenv: For managing environment variables and .env files
    - mnemonic: For generating mnemonic phrases

Note: This script assumes the existence of a .env file in the project root for
storing environment variables. If the file doesn't exist, it will be created
when saving a new key.
"""

# Import statements and code follow here...
import click
from dotenv import dotenv_values, load_dotenv, set_key
from mnemonic import Mnemonic


# Generate identity command
@click.command(name="generate-identity")
@click.option(
    "-s",
    "--strength",
    type=int,
    default=256,
    show_default=True,
    help="Strength of the mnemonic (128 or 256 bits)",
)
@click.option(
    "-n",
    "--name",
    default="AGENT_KEY",
    show_default=True,
    help="Name of the environment variable",
)
@click.option(
    "-o", "--output", type=click.Path(), help="Output file for saving the generated key"
)
def identity(strength, name, output):
    """Generate an agent identity key as a mnemonic phrase and optionally save to file or .env."""

    # Generate a mnemonic phrase for the identity key
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=strength)
    env_record = f'{name}="{words}"'

    # Output the generated key to the specified file or stdout
    if output:
        with open(output, "a") as f:
            f.write(env_record + "\n")
        click.echo(f"{name} ({strength} bits) appended to {output}")
    else:
        click.echo(env_record)

    # Load existing environment variables to check if the key already exists
    load_dotenv()
    existing_env = dotenv_values(".env")

    # Check if the key already exists in .env
    if name in existing_env:
        # Ask user to confirm overwrite
        if not click.confirm(
            f"{name} already exists in .env. Do you want to overwrite it?",
            default=False,
        ):
            click.echo("Key not saved to .env.")
            return

    # Save the key to .env
    set_key(".env", name, words)
    click.echo(f"{name} saved to .env.")
