import json
from typing import Any, Type

import boto3
from pydantic import BaseModel, ValidationError

from models.prompt import MessageType, Prompt


class BedrockChatService:
    def __init__(self, inference_profile_arn, region_name="us-east-1"):
        self.inference_profile_arn = inference_profile_arn
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime", region_name=region_name
        )

    def chat(self, prompt: Prompt):
        """
        Send a message to the Bedrock model and return the response.
        Reference for messages' format can be found at:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html
        """
        system, messages = self.__build_messages(prompt)

        response = self.bedrock_runtime.converse(
            modelId=self.inference_profile_arn,
            messages=messages,
            system=system,
        )
        return response["output"]["message"]["content"][0]["text"]

    def structural_chat(
        self, prompt: Prompt, output_model: Type[BaseModel]
    ) -> BaseModel:
        """
        Send a message to the Bedrock model and return the response in a schema that aligns with the provided model.
        Use the tool_options in request to force a "tool_use" response from the model.
        Then use the tool_request to get the structured output.
        https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-examples.html
        For complete list of models that support tool use, refer to:
        https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-supported-models-features.html
        """
        system, messages = self.__build_messages(prompt)
        tool_config = self.__build_tool_config(output_model)
        response = self.bedrock_runtime.converse(
            modelId=self.inference_profile_arn,
            messages=messages,
            system=system,
            toolConfig=tool_config,
        )

        # The model will respond with a `toolUse` block.
        content_blocks = response["output"]["message"]["content"]

        tool_use_block = next(
            block["toolUse"] for block in content_blocks if "toolUse" in block
        )
        # This is your JSON object, already parsed and matching the schema
        if "input" in tool_use_block:
            print("Tool use block found with input.")
            result = tool_use_block["input"]
        else:
            print("No tool use block found, falling back to text content.")
            result = content_blocks[0]["text"]

        print(f"Raw tool use result: {result}")

        validated_data = self.__create_model(result, output_model)
        return validated_data

    def __build_messages(self, prompt: Prompt):
        system = []
        messages = []
        for message in prompt.messages:
            content = {"text": message.content}
            if message.type == MessageType.SYSTEM:
                system.append(content)
            else:
                role = message.type.value
                messages.append({"role": role, "content": [content]})
        return system, messages

    def __build_tool_config(
        self, output_model: Type[BaseModel], support_tool_choice_tool: bool = False
    ) -> dict:
        json_schema = output_model.model_json_schema()
        tool_name = "json_output_tool"
        tool_config = {
            "tools": [
                {
                    "toolSpec": {
                        "name": tool_name,
                        "description": "Get the JSON output that align with the provided schema.",
                        "inputSchema": {"json": json_schema},
                    }
                }
            ]
        }
        # Optional but useful: force the model to use THIS tool
        if support_tool_choice_tool:
            tool_config["toolChoice"] = {"tool": {"name": tool_name}}
        return tool_config

    def __create_model(self, data: Any, model: Type[BaseModel]) -> BaseModel | None:
        if isinstance(data, (str, bytes)):
            try:
                model_instance = model.model_validate_json(data)
                return model_instance
            except (ValidationError, json.JSONDecodeError) as e:
                print(f"Error validating JSON string: {e}")
                return None
        elif isinstance(data, dict):
            try:
                model_instance = model.model_validate(data)
                return model_instance
            except ValidationError as e:
                print(f"Error validating dictionary: {e}")
                return None
        else:
            print(f"Input data is of an unsupported type: {type(data)}")
            return None
