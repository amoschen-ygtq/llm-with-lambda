from models.online_course import OnlineCourse
from services.ollama_chat_service import OllamaChatService
from services.prompt_service import PromptService
from services.web_scraper_service import WebScraperService

URL = "https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models"

scraper = WebScraperService()
chat_service = OllamaChatService()
prompt_service = PromptService()

text_content = scraper.scrape_plain_text(URL)
if text_content:
    example = OnlineCourse(
        title="Example Course",
        instructor="John Doe",
        platform="Udemy",
        url="https://www.udemy.com/course/example-course",
        description="This is an example course description.",
    )
    summarization_prompt = (
        prompt_service.build_content_summarization_prompt_for_structural_output(
            text_content,
            example,
        )
    )
    reply = chat_service.structural_chat(summarization_prompt, OnlineCourse)
    print(reply.model_dump_json(indent=2))
else:
    print("Failed to retrieve or parse content from the URL.")
