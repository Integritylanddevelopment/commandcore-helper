import os
import time
from typing import Dict, List
import openai

# Load OpenAI API key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to interact with OpenAI API
def run_agent(prompt: str, config: Dict):
    """Run the agent logic using OpenAI's API."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": config.get("system_prompt", "")},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

def batch_and_throttle_requests(prompts: List[str], config: Dict, delay: float = 1.0):
    """Batch and throttle requests to the OpenAI API."""
    results = []
    for prompt in prompts:
        result = run_agent(prompt, config)
        results.append(result)
        time.sleep(delay)  # Throttle requests by introducing a delay
    return results
