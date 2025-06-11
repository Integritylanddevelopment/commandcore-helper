from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "social_bot",
    "style": "structured",
    "system_prompt": (
        "You are a social bot. Your task is to craft engaging social media posts and strategies tailored to target audiences. "
        "Focus on maximizing reach and driving interactions."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for social media strategy analysis."""
    return f"Social media context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable social media strategies."""
    return f"### Social Media Strategies\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
