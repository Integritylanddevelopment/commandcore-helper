from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "voice_consistency_bot",
    "style": "structured",
    "system_prompt": (
        "You are a voice consistency bot. Your task is to ensure consistent tone and style across all communications. "
        "Analyze the input and provide suggestions to align with the desired voice guidelines."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to align with voice guidelines
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result to ensure actionable voice consistency suggestions
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Align the input prompt with voice guidelines."""
    return f"Voice guidelines applied: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable voice consistency suggestions."""
    return f"### Voice Consistency Suggestions\n{result.strip()}"
