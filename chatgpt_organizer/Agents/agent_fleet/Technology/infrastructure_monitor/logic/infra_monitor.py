from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "infra_monitor",
    "style": "structured",
    "system_prompt": (
        "You are an infrastructure monitor bot. Your task is to analyze system logs and metrics to identify potential issues and "
        "recommend optimizations for system performance and reliability."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for infrastructure monitoring."""
    return f"Infrastructure monitoring context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable infrastructure recommendations."""
    return f"Infrastructure Recommendations: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
