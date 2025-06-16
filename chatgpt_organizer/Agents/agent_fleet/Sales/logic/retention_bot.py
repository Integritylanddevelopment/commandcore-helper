from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "retention_bot",
    "style": "structured",
    "system_prompt": (
        "You are a retention bot. Your task is to analyze customer behavior and provide actionable insights to improve retention rates. "
        "Focus on identifying churn risks and suggesting personalized engagement strategies."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for retention analysis."""
    return f"Retention analysis context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable retention insights."""
    return f"Retention Insights: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
