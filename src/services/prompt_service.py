from pydantic import BaseModel

from models.prompt import Message, MessageType, Prompt


class PromptService:
    def __init__(self):
        pass

    def build_content_summarization_prompt(self, text_content: str) -> Prompt:
        """
        Build a prompt for summarizing the given text content.
        """
        messages = [
            Message(type=MessageType.SYSTEM, content="You are a helpful assistant."),
            Message(
                type=MessageType.USER,
                content=("Please summarize the following content:\n\n" + text_content),
            ),
        ]
        return Prompt(version="1.0", messages=messages)

    def build_content_summarization_prompt_for_structural_output(
        self, text_content: str, example: BaseModel
    ) -> Prompt:
        """
        Build a prompt for summarizing the given text content into a structured format
        according to the provided example model.
        """
        messages = [
            Message(type=MessageType.SYSTEM, content="You are a helpful assistant."),
            Message(
                type=MessageType.USER,
                content=(
                    "Extract the details of the online course from the following content "
                    "and structure output into a JSON format according to the OnlineCourse model:\n\n"
                    + text_content
                    + "\n\n"
                    "Here is an example of the OnlineCourse model:\n"
                    f"{example.model_dump_json(indent=2)}"
                ),
            ),
        ]
        return Prompt(version="1.0", messages=messages)
