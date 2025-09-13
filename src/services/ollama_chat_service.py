from ollama import Client

class OlamaChatService:
    def __init__(self, host='http://host.docker.internal:11434', model='llama3.2'):
        self.client = Client(host=host)
        self.model = model

    def chat(self, user_message):
        response = self.client.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': user_message}]
        )
        return response['message']['content']
