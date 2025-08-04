from setuptools import setup, find_packages

setup(
    name="telegram_llm_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.4",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
    ],
)
