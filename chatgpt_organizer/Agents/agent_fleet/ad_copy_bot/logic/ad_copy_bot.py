from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "ad_copy_bot",
    "style": "structured",
    "system_prompt": (
        "You are an ad copy bot. Your task is to write high-conversion ad copy tailored for Google Ads, Facebook/Instagram Ads, "
        "and other PPC platforms, targeting user intent and emotional triggers."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for ad copy creation."""
    return f"Ad copy context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable ad copy suggestions."""
    return f"### Ad Copy Suggestions\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
