# Single Shot Agent

This is an example agent that will receive a single message and reply to it.
There is no conversation context to this agent.

# Requirements

You must have Python 3.13 installed, run the following to confirm:

```shell
python --version
```

You must be in the single-shot-agent directory, run the following to confirm:

```shell
pwd
```

The result should show the `fetchai/examples/single-shot-agent` directory.

# Set up Enviroment

First set up your environment. Ensure you have Pyton 3.13 installed and run

```shell
poetry install
```

# Running the tests

Run the Unit Tests to confirm that everything is installed correctly:

```shell
poetry run pytest .
```

# Run the agent

```shell
poetry run dev_agent
```

This will run your agent in development mode. You can test that it is running by
visiting "http://localhost:8000" in your browser, or running the following curl 
command in another shell:

```shell
curl localhost:8000
```

You should see something like `{"status":"OK"}` returned.
