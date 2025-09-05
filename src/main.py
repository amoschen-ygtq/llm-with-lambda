from ollama import Client

# Specify the host URL for Ollama's REST API
client = Client(host='http://host.docker.internal:11434')

# Send user prompt to Llama 3.2 model
response = client.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'Hello from the devcontainer with Pipenv!'}]
)
print(response['message']['content'])