"""
This module initializes and exposes the core services for the application.

Imports:
    OlamaChatService: Service for handling chat interactions using Ollama.
    WebScraperService: Service for scraping web content.

Note:
    The imports make these services available for use throughout the package.
"""

from .ollama_chat_service import OlamaChatService
from .web_scraper_service import WebScraperService