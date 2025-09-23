from ollama import Client

from models.prompt import Prompt


class OllamaChatService:
    def __init__(self, host="http://host.docker.internal:11434", model="llama3.2"):
        self.client = Client(host=host)
        self.model = model

    def chat(self, prompt: Prompt):
        messages = []
        for message in prompt.messages:
            role = message.type.value or "user"  # Default to user if unknown type
            messages.append({"role": role, "content": message.content})

        response = self.client.chat(
            model=self.model,
            messages=messages,
        )
        return response["message"]["content"]
