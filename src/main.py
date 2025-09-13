from services import OlamaChatService
from services import WebScraperService

URL = 'https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models'

scraper = WebScraperService()
text_content = scraper.scrape_plain_text(URL)
if text_content:
    chat_service = OlamaChatService()
    user_message = f"Please summarize the following content:\n\n{text_content}"
    reply = chat_service.chat(user_message)
    print(reply)
else:
    print("Failed to retrieve or parse content from the URL.")
