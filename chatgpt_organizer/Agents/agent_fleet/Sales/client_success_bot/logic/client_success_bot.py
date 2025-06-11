from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "client_success_bot",
    "style": "structured",
    "system_prompt": (
        "You are a client success bot. Your task is to analyze client interactions and provide actionable insights to improve "
        "client satisfaction and retention."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for client success analysis."""
    return f"Client success context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable client success strategies."""
    return f"Client Success Strategies: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
