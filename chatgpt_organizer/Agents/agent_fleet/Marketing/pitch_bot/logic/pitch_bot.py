from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "pitch_bot",
    "style": "structured",
    "system_prompt": (
        "You are a pitch bot. Your task is to craft compelling pitches tailored to specific audiences and objectives. "
        "Focus on maximizing impact and engagement."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for pitch creation analysis."""
    return f"Pitch context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable pitch strategies."""
    return f"### Pitch Strategies\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
