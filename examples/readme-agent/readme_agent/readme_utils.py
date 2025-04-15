import openai

from readme_agent.settings import OPENAI_API_KEY


def extract_readme(readme_metadata: str) -> str:
    """
    Extracts those pieces from an agent readme that are actually relevant when searching agents based on a short search text.
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""Extract the most relevant from this agent readme:
    {readme_metadata}
    Return only the relevant general information of what the agent is used for in plain text.
    Don't include the name of the parameters etc, only the general purpose of the agent.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant who wants to extract only those pieces from an agent readme
                that are relevant when searching agent readmes based on a short search text.""",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    readme = response.choices[0].message.content.strip()
    print("Readme:", readme)

    return readme
