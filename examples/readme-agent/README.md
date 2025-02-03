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

If you are running the example locally, you will need a publicly available url. The simplest
way to achieve this is to use a tool like [ngrok](https://ngrok.com/) which you can configure
to proxy a local url to a public url.

### Local environment

Copy the `.env.example` file to `.env` and populate with your own values for each Key.

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

## Run ngrok or similar to make it available on the internet

## Register your agent on Agentverse

## Send a message to your agent via Agentverse

