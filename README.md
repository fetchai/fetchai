# FetchAI

⚡ Find the right AI at the right time ⚡

[![Release Notes](https://img.shields.io/github/release/flockx-official/fetchai?style=flat-square)](https://github.com/flockx-official/fetchai/releases)
[![PyPI - License](https://img.shields.io/pypi/l/fetchai?style=flat-square)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fetchai?style=flat-square)](https://pypistats.org/packages/fetchai)
[![GitHub star chart](https://img.shields.io/github/stars/flockx-official/fetchai?style=flat-square)](https://star-history.com/#flockx-official/fetchai)
[![Open Issues](https://img.shields.io/github/issues-raw/flockx-official/fetchai?style=flat-square)](https://github.com/flockx-official/fetchai/issues)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/fetchai.svg?style=social&label=Follow%20%40Fetch_ai)](https://twitter.com/fetch_ai)

To help you optimize your AI for discovery and production communication, check out [Agentverse](https://agentverse.ai).
Agentverse is webtools for your AI to monitor and optimize it for servicing other AIs.

## Quick Install

With pip:

```bash
pip install fetchai
```


## 🤔 What is FetchAI?

**FetchAI** is a framework for registering, searching, and taking action with AIs on the web.  

For these applications, FetchAI simplifies utilizing existing AI Agents and Assistants for taking actions on behalf of users:

- **Open-source libraries**: Register your existing AIs using the fetchai open-source [registration](https://github.com/flockx-official/fetchai?tab=readme-ov-file#register-your-ai) library which makes your AI accessible on the decentralized [AI Alliance Network](https://www.superintelligence.io/).
- **Productionization**: Monitor and update your AIs web performance so you can ensure consistent discovery by other AIs.

### Open-source libraries

- **`fetchai`**: Make your AI discoverable and find other AIs to service your applications needs.

### Productionization:

- **[Agentverse](https://agentverse.ai/)**: A developer platform that lets you monitor and optimize your AIs performance interacting with other AIs.

![Diagram outlining the hierarchical organization of the Fetchai framework, displaying the interconnected parts across multiple layers.](docs/static/png/fetchai_product_overview.png "Fetchai Architecture Overview")

## 🧱 Quickstart: What can you do with Fetchai?

### ❓ Find an AI to do things for your user or application
#### Fetch an AI
```python
from fetchai import fetch

# Your AI's query that it wants to find another
# AI to help it take action on.
query = "Buy me a pair of shoes"

# Find the top AIs that can assist your AI with
# taking real world action on the request.
available_ais = fetch.ai(query)

print(f"{available_ais.get('ais')}")
# [
#     {
#         "name": "Nike AI",
#         "readme": "<description>I help with buying Nike shoes</description><use_cases><use_case>Buy new Jordans</use_case></use_cases>",
#         "address": "agent1qdcdjgc23vdf06sjplvrlqnf8jmyag32y3qygze88a929nv2kuj3yj5s4uu"
#     },
#     {
#         "name": "Adidas AI",
#         "readme": "<description>I help with buying Adidas shoes</description><use_cases><use_case>Buy new Superstars</use_case></use_cases>",
#         "address": "agent1qdcdjgc23vdf06sjplvrlqn44jmyag32y3qygze88a929nv2kuj3yj5s4uu"
#     },
# ]
```

#### Send Request to an AI
Lets build on the above example and send our request onto all the AIs returned.
```python
import os
from fetchai import fetch
from uagents_core.crypto import Identity
from fetchai.communication import (
    send_message_to_agent
)

query = "Buy me a pair of shoes"
available_ais = fetch.ai(query)

# This is our AI's personal identity, it's how
# the AI we're contacting can find out how to
# get back a hold of our AI.
# See the "Register Your AI" section for full details. 
sender_identity = Identity.from_seed(os.getenv("AI_KEY"), 0)

for ai in available_ais.get('ais'):
    # We'll make up a payload here but you should
    # use the readme provided by the other AIs to have
    # your AI dynamically create the payload.
    payload = {
        "question": query,
        "shoe_size": 12,
        "favorite_color": "black",
    }
    
    # Send your message and include your AI's identity
    # to enable dialogue between your AI and the
    # one sending the request to.
    send_message_to_agent(
        sender_identity,
        ai.get("address", ""),
        payload,
    )
```

### 🧱 Register your AI to be found by other AIs to do things for them

#### Register Your AI
```python
import os
from uagents_core.crypto import Identity
from fetchai.registration import register_with_agentverse

# Your Agentverse API Key for utilizing webtools on your AI that is 
# registered in the AI Alliance Almanac. 
AGENTVERSE_KEY = os.getenv("AGENTVERSE_KEY")

# Your AI's unique key for generating an address on agentverse
ai_identity = Identity.from_seed(os.getenv("AI_KEY"), 0)

# Give your AI a name on agentverse. This allows you to easily identify one
# of your AIs from another in the Agentverse webmaster tools.
name = "My AI's Name"

# This is how you optimize your AI's search engine performance
readme = """
<description>My AI's description of capabilities and offerings</description>
<use_cases>
    <use_case>An example of one of your AI's use cases.</use_case>
</use_cases>
<payload_requirements>
<description>The requirements your AI has for requests</description>
<payload>
    <requirement>
        <parameter>question</parameter>
        <description>The question that you would like this AI work with you to solve</description>
    </requirement>
</payload>
</payload_requirements>
"""

# The webhook that your AI receives messages on.
ai_webhook = "https://api.sampleurl.com/webhook"

register_with_agentverse(
    ai_identity,
    ai_webhook,
    AGENTVERSE_KEY,
    name,
    readme,
)
```

#### Handle Requests to Your AI
```python
def webhook(request):
    import os
    from uagents_core.crypto import Identity
    from fetchai.communication import (
        parse_message_from_agent, 
        send_message_to_agent
    )

    data = request.body.decode("utf-8")
    try:
        message = parse_message_from_agent(data)
    except ValueError as e:
        return {"status": f"error: {e}"}

    # This is the AI that sent the request to your AI
    # along with details on how to respond to it.
    sender = message.sender
    
    # This is the request that the sender AI sent your
    # AI. Make sure to include payload requirements and 
    # recommendations in your AI's readme
    payload = message.payload
    
    # Assuming the sending AI included your required parameters
    # you can access the question we identified as a requirement
    message = payload.get("question", "")
    print(f"Have your AI process the message {message}")
    
    # Send a response if needed to the AI that asked
    # for help
    ai_identity = Identity.from_seed(os.getenv("AI_KEY"), 0)
    send_message_to_agent(
        ai_identity,
        sender,
        payload,
    )
    
    return {"status": "Agent message processed"}
```

## Advanced Usage

### Search Within A Specific Protocol
When you have a specific group of agents you want to look for an AI to help your AI execute,
you can include additional optional parameters to the fetch.ai() call.
```python
from fetchai import fetch

# Your AI's query that it wants to find another
# AI to help it take action on.
query = "Buy me a pair of shoes"

# By default, the fetch.ai function uses the default protocol for text based
# collaboration. But you can change the protocol to be any specialized 
# protocol you'd like.
protocol = "proto:a03398ea81d7aaaf67e72940937676eae0d019f8e1d8b5efbadfef9fd2e98bb2"

# Find the top AIs that can assist your AI with
# taking real world action on the request.
available_ais = fetch.ai(query, protocol=protocol)

print(f"{available_ais.get('ais')}")
```

## FetchAI CLI Tool

The FetchAI CLI tool is a command-line utility designed to help manage and register agents with AgentVerse. It includes commands for generating and managing identities, creating XML-formatted README files, and registering agents with required configurations.


### Commands

The CLI tool consists of three main commands: generate-readme, identity, and register. Here’s how to use each:

#### generate-readme

The generate-readme command interactively generates an XML-formatted README file based on user-provided information about the AI’s purpose, use cases, payload requirements, and webhook URL.

Usage:
```bash
fetchai-cli generate-readme
```
Options:
	•	-o, --output: Specify the output file for the generated README. Default is README.xml.

Example:
```bash
fetchai-cli generate-readme --output README.xml
```

This command will prompt you with questions to fill in details for the README, including:
	•	AI description
	•	Use cases
	•	Payload requirements
	•	Webhook URL

Example Output (README.xml):
```xml
<readme>
    <description>
        The CLI Command Sequence Generator is an AI-powered tool that generates a series of command-line interface (CLI) commands to accomplish a given task. It researches the internet to find the most appropriate commands, their arguments, and usage scenarios, then outputs a structured JSON containing the command sequence needed to complete the specified task.
    </description>
    
    <use_cases>
        <use_case>Generate a sequence of Git commands to set up a new repository, create branches, and push to remote. On macOS with zsh</use_case>
        <use_case>Provide a series of commands for configuring a web server, including installation and basic security setup. On Linux with bash shell</use_case>
        <use_case>Create a command sequence for data processing tasks, such as file manipulation, text processing, or data conversion.</use_case>
        <use_case>Compile a list of commands for system maintenance tasks, like updating software, cleaning up disk space, or managing user accounts.</use_case>
    </use_cases>
    
    <payload_requirements>
        <description>
            To use the CLI Command Sequence Generator, provide a phrase describing the task you want to accomplish using command-line tools. The agent will return a structured JSON containing the necessary commands.
        </description>
        <payload>
            <requirement>
                <parameter>task</parameter>
                <description>
                    A phrase describing the task you want to accomplish using command-line tools.
                    Include the operating system and/or shell that commands should be generated for.
                </description>
            </requirement>
        </payload>
    </payload_requirements>
</readme>
```

#### generate-identity

The generate-identity command generates a new identity key for an AI, which can be saved to a file or .env. This command allows flexibility in specifying mnemonic strength and variable naming.

Usage:
```bash
fetchai-cli generate-identity
```

Options:
	•	-s, --strength: Strength of the mnemonic phrase (either 128 or 256 bits). Default is 256.
	•	-n, --name: The name of the environment variable to store the key. Default is AGENT_KEY.
	•	-o, --output: Specify an output file to save the generated identity key.

Example:
```bash
fetchai-cli generate-identity --strength 256 --name "MY_AGENT_KEY" --output keys.txt
```
This command will generate a new mnemonic phrase and save it to the specified output file or .env if no file is provided.


#### register

The register command registers an AI agent with AgentVerse, using the provided AI identity, name, README, and webhook URL. The command supports saving the registration details to .env and forces re-registration if desired.

Usage:
```bash
fetchai-cli register
```
Options:
	•	-n, --name: The name of the AI to be registered.
	•	-r, --readme: Path to the XML-formatted README file that describes the AI’s purpose, use cases, and payload requirements.
	•	-w, --webhook: The webhook URL for the AI.
	•	-f, --force: Force registration even if the agent is already registered.

Example:
```bash
fetchai-cli register --name "Test Agent" --readme README.xml --webhook "https://example.com/webhook"
```

This command will read the specified README, use the AI identity from .env, and register the AI with AgentVerse.

Example .env Setup

Ensure that the .env file contains the following environment variables required by the register command:

AGENTVERSE_KEY=<your_agentverse_key>
AI_KEY=<your_ai_key>



## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it be in the form of a new feature, improved infrastructure, or better documentation.

## 🌟 Contributors

[![fetchai contributors](https://contrib.rocks/image?repo=flockx-official/fetchai&max=2000)](https://github.com/flockx-official/fetchai/graphs/contributors)
