import json
import boto3
import os

# Your inference profile ARN from Step 1
INFERENCE_PROFILE_ARN = "Placeholder for inference profile ARN"
DEFAULT_PROMPT = "Give me a fun fact about serverless technology."

# The Bedrock Runtime client to invoke the model
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.environ.get('us-east-1')
)

def lambda_handler(event, context):
    """
    Invokes a Bedrock model using an inference profile and returns the response.
    """
    # Extract the user prompt from the Lambda event payload
    prompt = event.get('prompt', DEFAULT_PROMPT)

    # The message payload for the Converse API
    messages = [{"role": "user", "content": [{"text": prompt}]}]

    try:
        response = bedrock_runtime.converse(
            modelId=INFERENCE_PROFILE_ARN,  # Use the profile ARN here
            messages=messages
        )

        # Extract the content from the response
        output_message = response['output']['message']['content'][0]['text']

        return {
            'statusCode': 200,
            'body': json.dumps({'response': output_message})
        }

    except Exception as e:
        print(f"Error invoking Bedrock model: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }