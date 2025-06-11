from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "ux_writer",
    "style": "structured",
    "system_prompt": (
        "You are a UX writer bot. Your task is to craft user-friendly and engaging text for interfaces. "
        "Analyze the input and provide suggestions to improve clarity, tone, and usability."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for UX writing analysis."""
    return f"UX writing context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable UX writing suggestions."""
    return f"### UX Writing Suggestions\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
