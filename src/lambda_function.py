import json
import os

from services.bedrock_chat_service import BedrockChatService
from services.prompt_service import PromptService
from services.web_scraper_service import WebScraperService

# Your inference profile ARN from Step 1
INFERENCE_PROFILE_ARN = os.environ.get("INFERENCE_PROFILE_ARN", None)
if INFERENCE_PROFILE_ARN is None:
    raise ValueError("INFERENCE_PROFILE_ARN environment variable is not set.")

DEFAULT_URL = (
    "https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models"
)

# Initialize Bedrock service in global scope
bedrock_service = BedrockChatService(inference_profile_arn=INFERENCE_PROFILE_ARN)
scraper_service = WebScraperService()
prompt_service = PromptService()


def lambda_handler(event, context):
    """
    Scrapes text content from a given URL and sends it to a Bedrock model for processing.
    """
    # Extract the user prompt from the Lambda event payload
    url = event.get("url", DEFAULT_URL)
    try:
        text_content = scraper_service.scrape_plain_text(url)
    except Exception as e:
        print(f"Error scraping URL: {e}")
        text_content = None

    summarization_prompt = prompt_service.build_content_summarization_prompt(
        text_content
    )
    try:
        output_message = bedrock_service.send_message(summarization_prompt)
        return {"statusCode": 200, "body": json.dumps({"response": output_message})}
    except Exception as e:
        print(f"Error invoking Bedrock model: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
