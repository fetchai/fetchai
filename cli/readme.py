"""
readme.py

This module provides functionality for generating and managing README files for AI agents
within the FetchAI CLI tool. It offers a command-line interface for creating structured
XML README files and utilities for loading existing README content.

Main Components:
1. generate-readme command: Generates an XML-formatted README file based on user input.
2. load_readme function: Utility for loading content from existing README files.

Usage:
    python -m fetchai.cli generate-readme [OPTIONS]

Options:
    -o, --output PATH  Output file for the generated README in XML format [default: README.xml]
    --help             Show this message and exit.

The README generation process includes:
1. Prompting the user for AI name, description, use cases, and payload requirements
2. Creating an XML structure with the provided information
3. Writing the formatted XML to the specified output file

Key Features:
- Interactive command-line interface for gathering AI information
- Structured XML output for consistent README formatting
- Support for multiple use cases and payload parameters
- Pretty-printing of XML for improved readability
- Error handling for file operations

Functions:
    readme(output): Main function for generating the README XML file.
    load_readme(file_path): Utility function to load existing README content.

Dependencies:
    - click: For creating the command-line interface
    - xml.etree.ElementTree: For creating XML structures
    - xml.dom.minidom: For pretty-printing XML

Note: This script assumes that the user has the necessary information about their AI agent
ready when running the generate-readme command. The generated README.xml file should be
reviewed and potentially edited for completeness and accuracy after generation.
"""

import sys
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring

import click


@click.command(name="generate-readme")
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="README.xml",
    show_default=True,
    help="Output file for the generated README in XML format",
)
def readme(output):
    """Generate a README XML file for the AI with user inputs."""

    # Prompt the user for necessary information
    name = click.prompt("Enter the AI's name")
    description = click.prompt(
        "Enter a description of the AI's capabilities and offerings"
    )

    # Use cases
    use_cases = []
    while True:
        use_case = click.prompt(
            "Enter a use case (or leave blank to finish)",
            default="",
            show_default=False,
        )
        if not use_case:
            break
        use_cases.append(use_case)

    # Payload requirements
    payload_description = click.prompt(
        "Enter a description for the payload requirements"
    )
    payload_requirements = []
    while True:
        parameter = click.prompt(
            "Enter a payload parameter name (or leave blank to finish)",
            default="",
            show_default=False,
        )
        if not parameter:
            break
        parameter_description = click.prompt(
            f"Enter a description for parameter '{parameter}'"
        )
        payload_requirements.append((parameter, parameter_description))

    # Create XML structure
    root = Element("readme")

    # Description
    description_elem = SubElement(root, "description")
    description_elem.text = description

    # Use Cases
    use_cases_elem = SubElement(root, "use_cases")
    for use_case in use_cases:
        use_case_elem = SubElement(use_cases_elem, "use_case")
        use_case_elem.text = use_case

    # Payload Requirements
    payload_elem = SubElement(root, "payload_requirements")

    payload_desc_elem = SubElement(payload_elem, "description")
    payload_desc_elem.text = payload_description

    payload_sub_elem = SubElement(payload_elem, "payload")
    for parameter, param_desc in payload_requirements:
        requirement_elem = SubElement(payload_sub_elem, "requirement")

        param_elem = SubElement(requirement_elem, "parameter")
        param_elem.text = parameter

        param_desc_elem = SubElement(requirement_elem, "description")
        param_desc_elem.text = param_desc

    # Convert to a pretty XML string
    raw_xml = tostring(root, "utf-8")
    pretty_xml = parseString(raw_xml).toprettyxml(indent="    ")

    # Write to output file
    with open(output, "w") as f:
        f.write(pretty_xml)
    click.echo(f"README generated and saved to {output}")


# Utility function to load README content
def load_readme(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        click.echo(f"Error: README file not found at {file_path}")
        sys.exit(1)
    except IOError:
        click.echo(f"Error: Unable to read README file at {file_path}")
        sys.exit(1)
