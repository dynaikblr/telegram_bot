# bot.py

import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import config
from llm_handler import LLMHandler

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Main bot class for handling Telegram interactions via webhook."""

    def __init__(self):
        """Initialize the bot with handlers."""
        self.llm = LLMHandler()
        self.application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        # Initialize conversation history dictionary
        self.conversations = {}

        # Register command and message handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Respond to /start command."""
        await update.message.reply_text(
            "👋 Hello! I'm your AI assistant. Send me a message and I'll respond using LLM."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Provide help info."""
        help_text = (
            "🤖 Bot Commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "Simply send me any message and I'll respond using AI!"
        )
        await update.message.reply_text(help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Receive messages and forward to LLM."""
        try:
            user_id = update.message.from_user.id
            user_message = update.message.text
            user_name = update.message.from_user.first_name
            logger.info(f"Received message from {user_name} (ID: {user_id}): {user_message}")

            # Initialize conversation history for new users
            if user_id not in self.conversations:
                self.conversations[user_id] = []

            # Add user message to history
            self.conversations[user_id].append({
                "role": "user",
                "content": user_message
            })

            # Keep only last 6 turns (12 messages - 6 from user, 6 from assistant)
            if len(self.conversations[user_id]) > 12:
                self.conversations[user_id] = self.conversations[user_id][-12:]

            # Get response using full conversation history
            response = self.llm.get_response(self.conversations[user_id])
            logger.info(f"Bot response to {user_name}: {response}")

            # Add assistant's response to history
            self.conversations[user_id].append({
                "role": "assistant",
                "content": response
            })

            await update.message.reply_text(response)

        except Exception as e:
            logger.exception("Error while handling message")
            await update.message.reply_text(
                "Sorry, I encountered an error while processing your message. Please try again later."
            )

    def run(self) -> None:
        """Start the bot via webhook binding for Render."""
        port = int(os.environ.get("PORT", 8443))
        webhook_url = f"{config.WEBHOOK_URL}/{config.TELEGRAM_TOKEN}"
        logger.info(f"Starting webhook on port {port}, URL: {webhook_url}")
        self.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url
        )
