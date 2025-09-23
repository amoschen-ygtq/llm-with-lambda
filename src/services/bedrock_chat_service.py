import boto3

from models.prompt import MessageType, Prompt


class BedrockChatService:
    def __init__(self, inference_profile_arn, region_name="us-east-1"):
        self.inference_profile_arn = inference_profile_arn
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime", region_name=region_name
        )

    def send_message(self, prompt: Prompt):
        """
        Send a message to the Bedrock model and return the response.
        Reference for messages' format can be found at:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html
        """
        system = []
        messages = []
        for message in prompt.messages:
            content = {"text": message.content}
            if message.type == MessageType.SYSTEM:
                system.append(content)
            else:
                role = message.type.value
                messages.append({"role": role, "content": [content]})

        response = self.bedrock_runtime.converse(
            modelId=self.inference_profile_arn,
            messages=messages,
            system=system,
        )
        return response["output"]["message"]["content"][0]["text"]
