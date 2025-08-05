"""Main entry point for the Telegram LLM bot."""

import sys
import logging
import telegram
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from bot import TelegramBot
import config

# Set up logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Create log file in the src directory
log_file = Path(__file__).parent / 'bot.log'
print(f"Initializing... Log will be written to: {log_file}")

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        # Log to console with DEBUG level
        logging.StreamHandler(sys.stdout),
        # Log to file
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG for more verbose output

def main():
    """Initialize and run the bot."""
    print("Starting bot initialization...")
    logger.info("Starting Telegram LLM Bot...")
    logger.info("python-telegram-bot version:", telegram.__version__)
    try:
        logger.debug("Creating TelegramBot instance...")
        print("Creating bot instance...")
        bot = TelegramBot()
        logger.info("Bot initialized successfully!")
        logger.debug("Configuration loaded with:")
        logger.debug(f"- Model: {config.MODEL}")
        logger.debug(f"- Base URL: {config.OPENROUTER_BASE_URL}")
        print("Bot is ready to start running...")
        logger.info("Bot is now running. Press Ctrl+C to stop.")
        print("Starting bot.run()...")
        bot.run()
    except Exception as e:
        error_msg = f"Error running bot: {str(e)}"
        print(f"ERROR: {error_msg}")
        logger.error(error_msg)
        raise

if __name__ == "__main__":
    main()
