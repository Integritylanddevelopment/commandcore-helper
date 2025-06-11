from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "keyword_miner",
    "style": "structured",
    "system_prompt": (
        "You are a keyword miner bot. Your task is to analyze content and extract high-value keywords for SEO and marketing purposes. "
        "Focus on identifying keywords with high search volume and relevance."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for keyword analysis."""
    return f"Keyword analysis context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable keyword strategies."""
    return f"Keyword Strategies: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
