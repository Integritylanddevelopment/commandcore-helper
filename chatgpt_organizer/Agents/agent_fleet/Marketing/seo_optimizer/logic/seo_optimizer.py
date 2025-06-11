from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "seo_optimizer",
    "style": "structured",
    "system_prompt": (
        "You are an SEO optimizer bot. Your task is to analyze website content and provide actionable recommendations to improve "
        "search engine rankings and organic traffic."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for SEO analysis."""
    return f"SEO context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable SEO strategies."""
    return f"SEO Strategies: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
