from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "marketing_bot",
    "style": "structured",
    "system_prompt": (
        "You are a marketing bot. Your task is to create compelling marketing strategies and campaigns tailored to target audiences. "
        "Focus on maximizing engagement and driving conversions."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for marketing strategy analysis."""
    return f"Marketing strategy context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable marketing strategies."""
    return f"### Marketing Strategies\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
