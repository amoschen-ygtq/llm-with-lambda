from services.ollama_chat_service import OllamaChatService
from services.prompt_service import PromptService
from services.web_scraper_service import WebScraperService

URL = "https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models"

scraper = WebScraperService()
chat_service = OllamaChatService()
prompt_service = PromptService()

text_content = scraper.scrape_plain_text(URL)
if text_content:
    summarization_prompt = prompt_service.build_content_summarization_prompt(
        text_content
    )
    reply = chat_service.chat(summarization_prompt)
    print(reply)
else:
    print("Failed to retrieve or parse content from the URL.")
