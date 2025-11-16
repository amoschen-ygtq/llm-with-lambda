from typing import Type

from ollama import Client
from pydantic import BaseModel

from models.prompt import Prompt


class OllamaChatService:
    def __init__(self, host="http://host.docker.internal:11434", model="llama3.2"):
        self.client = Client(host=host)
        self.model = model

    def chat(self, prompt: Prompt) -> str:
        messages = self.__build_messages(prompt)
        response = self.client.chat(
            model=self.model,
            messages=messages,
        )
        return response["message"]["content"]

    def structural_chat(
        self, prompt: Prompt, output_model: Type[BaseModel]
    ) -> BaseModel:
        messages = self.__build_messages(prompt)
        json_schema = output_model.model_json_schema()
        response = self.client.chat(
            model=self.model,
            messages=messages,
            format=json_schema,
        )
        json_output = response["message"]["content"]
        validated_data = output_model.model_validate_json(json_output)
        return validated_data

    def __build_messages(self, prompt: Prompt):
        messages = []
        for message in prompt.messages:
            role = message.type.value or "user"  # Default to user if unknown type
            messages.append({"role": role, "content": message.content})
        return messages
