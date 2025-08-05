"""LLM handler module for processing messages using Open Router API."""

import logging
from openai import OpenAI
import config

# Set up logging
logger = logging.getLogger(__name__)

class LLMHandler:
    """Handler for LLM interactions."""
    
    def __init__(self):
        """Initialize the LLM handler with Open Router configuration."""
        self.client = OpenAI(
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.OPENROUTER_API_KEY
        )
    
    def get_response(self, messages: list) -> str:
        """
        Get a response from the LLM based on the conversation history.
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content'
            
        Returns:
            str: The generated response
            
        Raises:
            Exception: If there's an error in getting the response
        """
        try:
            logger.info("Sending request to Open Router API...")
            # Prepend the system message to the conversation history
            full_messages = [{"role": "system", "content": config.SYSTEM_PROMPT}] + messages
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": config.SITE_URL,
                    "X-Title": config.SITE_NAME,
                },
                model=config.MODEL,
                messages=full_messages,
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE
            )
            logger.info("Received response from Open Router API")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            error_msg = f"Error getting LLM response: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
