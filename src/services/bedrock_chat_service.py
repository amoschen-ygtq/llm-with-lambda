import boto3

class BedrockChatService:
    def __init__(self, inference_profile_arn, region_name='us-east-1'):
        self.inference_profile_arn = inference_profile_arn
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )

    def send_message(self, prompt):
        messages = [{"role": "user", "content": [{"text": prompt}]}]
        response = self.bedrock_runtime.converse(
            modelId=self.inference_profile_arn,
            messages=messages
        )
        return response['output']['message']['content'][0]['text']