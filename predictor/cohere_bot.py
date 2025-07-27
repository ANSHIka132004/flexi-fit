import os
import cohere
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

def cohere_generate(prompt):
    try:
        response = co.generate(
            model="command-r-plus",  # Or "command-nightly" for experimental
            prompt=prompt,
            max_tokens=800,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error generating response: {e}"
