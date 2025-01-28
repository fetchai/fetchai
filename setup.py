from setuptools import setup, find_packages


setup(
    name="fetchai",
    version="0.1.18",
    packages=find_packages(exclude=("tests", "examples")),
    install_requires=[
        "bech32>=1.2.0,<2.0",
        "ecdsa>=0.19.0,<1.0",
        "pydantic>=2.7.4,<3.0",
        "requests>=2.32.3,<3.0",
        "httpx>=0.23.0,<1.0",
        "mnemonic>=0.21",
        "click>=8.1.2,<9.0",
        "python-dotenv>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "fetchai-cli = fetchai.cli:cli"  # Link to the main `cli` function in cli.py
        ]
    },
    extras_require={
        "dev": [
            "black==24.10.0",
            "pytest==8.3.4",
            "pytest-cov==6.0.0",
            "requests-mock==1.12.1",
        ],
    },
    description="Find the right AI at the right time and register your AI to be discovered.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flockx-official/fetchai",
    author="Devon Bleibtrey",
    author_email="bleib1dj@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
