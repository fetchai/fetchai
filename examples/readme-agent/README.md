# Readme Agent

This example shows how to use the fetchai sdk to create, publish and send 
messages to an agent.

## Setup

### Poetry

The example uses Poetry to create and manage your python environment, so make 
sure you have that installed. [Instructions](https://python-poetry.org/docs/#installation)

### Agentverse Account and API KEY

You will also need an agentverse account and API KEY, available [here](https://agentverse.ai/)

### Ngrok or similar if you are running your agent locally

If you are running the example locally, you will need a publicly available URL. The simplest
way to achieve this is to use a tool like [ngrok](https://ngrok.com/) which you can configure
to proxy a local URL to a public URL.

### Local environment

Copy the `.env.example` file to `.env` and populate with your own values for each key.

```shell
cp .env.example .env
```

### Install dependencies

From the `fetchai/examples/readme-agent` directory you can now install your environment and
test it is working by running the tests.

```shell
poetry install
poetry run pytest .
```

## Run your agent

Run your agent from the `fetchai/examples/readme-agent` directory with the following command:

```shell
poetry run fastapi dev readme_agent/agent.py
```

Your agent will run at [port 8000 on your localhost](http://127.0.0.1:8000/)

## Run ngrok or similar to make it available on the internet

To make this agent available on the internet, you should use something like ngrok, for example:

```shell
ngrok http --url=<Your Ngrok URL> 8000
```

You can set up your ngrok account [here](https://ngrok.com/) to get your url.

## Register your agent on Agentverse

Run the registration tool from the `fetchai/examples/readme-agent` directory:

```shell
poetry run python readme_agent/register_agent.py
```

You should see an output like this:

```shell
Registered agent at <Agentverse address>
```

## Send a message to your agent via Agentverse

You should be able to send a message to your agent now, using this command:

```shell
poetry run python readme_agent/send_message.py
```

