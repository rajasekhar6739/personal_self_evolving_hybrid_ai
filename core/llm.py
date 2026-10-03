import os
from openai import OpenAI

class GroqLLM:
    def __init__(self):
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY is not configured. Put it in .env")
        self.client = OpenAI(
            api_key=key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def ask(self, system, user, temperature=0.2):
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content.strip()
