from typing import Type

from ollama import Client
from pydantic import BaseModel

from models.prompt import Prompt


class OllamaChatService:
    def __init__(self, host="http://host.docker.internal:11434", model="llama3.2"):
        self.client = Client(host=host)
        self.model = model

    def chat(self, prompt: Prompt) -> str:
        """
        Send a message to the Ollama model and return the response.
        """
        messages = self.__build_messages(prompt)
        response = self.client.chat(
            model=self.model,
            messages=messages,
        )
        return response["message"]["content"]

    def structural_chat(
        self, prompt: Prompt, output_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Send a message to the Ollama model and return the response in a schema that aligns with the provided model.
        """
        messages = self.__build_messages(prompt)
        json_schema = output_model.model_json_schema()

        # Send the request with the desired JSON schema format
        response = self.client.chat(
            model=self.model,
            messages=messages,
            format=json_schema,
        )
        json_output = response["message"]["content"]

        # Validate and parse the JSON output into the specified Pydantic model
        validated_data = output_model.model_validate_json(json_output)
        return validated_data

    def __build_messages(self, prompt: Prompt):
        """
        Convert Prompt object to Ollama message format.
        """
        messages = []
        for message in prompt.messages:
            role = message.type.value or "user"  # Default to user if unknown type
            messages.append({"role": role, "content": message.content})
        return messages
