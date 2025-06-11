from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "content_curator",
    "style": "structured",
    "system_prompt": (
        "You are a content curator bot. Your task is to analyze and organize content to ensure relevance, quality, and engagement. "
        "Focus on creating cohesive and impactful content collections."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for content curation analysis."""
    return f"Content curation context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable content curation strategies."""
    return f"### Content Curation Strategies\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
