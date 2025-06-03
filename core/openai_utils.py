import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt3_completion(prompt, max_tokens=100):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()