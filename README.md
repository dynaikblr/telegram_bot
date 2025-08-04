# Telegram LLM Bot

A Telegram bot that integrates with Language Learning Models (LLMs) to provide intelligent responses.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your tokens:
```
TELEGRAM_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Running the Bot

```bash
python src/main.py
```

## Project Structure

```
telegram_llm_bot/
├── .github/
│   └── copilot-instructions.md
├── .vscode/
│   └── tasks.json
├── src/
│   ├── main.py
│   ├── config.py
│   ├── bot.py
│   └── llm_handler.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Features

- Telegram bot integration using python-telegram-bot
- Open Router API integration with Dolphin Mistral 24B model
- Environment-based configuration
- Error handling and logging
