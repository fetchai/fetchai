import openai

from readme_agent.settings import ASI1_URL, ASI1_API_KEY, ASI1_MODEL_NAME


def extract_readme(readme_metadata: str) -> str:
    """
    Extracts those pieces from an agent readme that are actually relevant when searching agents based on a short search text.
    """

    client = openai.OpenAI(api_key=ASI1_API_KEY, base_url=ASI1_URL)

    prompt = f"""Extract the most relevant from this agent readme:
    {readme_metadata}
    Return only the relevant general information of what the agent is used for in plain text.
    Don't include the name of the parameters etc, only the general purpose of the agent.
    """

    response = client.chat.completions.create(
        model=ASI1_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant who wants to extract only those pieces from an agent readme
                that are relevant when searching agent readmes based on a short search text.""",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    readme = response.choices[0].message.content.strip()

    return readme
