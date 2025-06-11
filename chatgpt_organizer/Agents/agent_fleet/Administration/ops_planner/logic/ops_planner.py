from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "ops_planner",
    "style": "structured",
    "system_prompt": (
        "You are an operations planner bot. Your task is to analyze operational workflows and provide actionable recommendations "
        "to optimize efficiency and resource allocation."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for operations planning analysis."""
    return f"Operations context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable operations planning strategies."""
    return f"Operations Planning Strategies: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
