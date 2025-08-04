"""Telegram bot module for handling user interactions."""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import config
from llm_handler import LLMHandler

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Main bot class for handling Telegram interactions."""
    
    def __init__(self):
        """Initialize the bot with necessary handlers."""
        self.llm = LLMHandler()
        self.application = Application.builder().token(config.TELEGRAM_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command."""
        await update.message.reply_text(
            "👋 Hello! I'm your AI assistant. Send me a message and I'll respond using advanced language models."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /help command."""
        help_text = """
🤖 Bot Commands:
/start - Start the bot
/help - Show this help message

Simply send me any message and I'll respond using AI!
        """
        await update.message.reply_text(help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle incoming messages."""
        try:
            # Get user message and info
            user_message = update.message.text
            user_name = update.message.from_user.first_name
            logger.info(f"Received message from {user_name}: {user_message}")
            
            # Get response from LLM
            response = self.llm.get_response(user_message)
            logger.info(f"Bot response: {response}")
            
            # Send response back to user
            await update.message.reply_text(response)
            
        except Exception as e:
            error_msg = f"Error handling message: {str(e)}"
            logger.error(error_msg)
            await update.message.reply_text(
                "Sorry, I encountered an error while processing your message. Please try again later."
            )
    
    def run(self) -> None:
        """Run the bot."""
        self.application.run_polling()
