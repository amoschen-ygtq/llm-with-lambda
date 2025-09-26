from models.prompt import Message, MessageType, Prompt


class PromptService:
    def __init__(self):
        pass

    def build_content_summarization_prompt(self, text_content: str) -> Prompt:
        messages = [
            Message(type=MessageType.SYSTEM, content="You are a helpful assistant."),
            Message(
                type=MessageType.USER,
                content=("Please summarize the following content:\n\n" + text_content),
            ),
        ]
        return Prompt(version="1.0", messages=messages)
