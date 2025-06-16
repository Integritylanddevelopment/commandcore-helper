from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "pulse_bot",
    "style": "structured",
    "system_prompt": (
        "You are a pulse bot. Your task is to analyze team sentiment and engagement levels based on input data. "
        "Provide actionable insights to improve morale and collaboration."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for sentiment analysis."""
    return f"Pulse analysis context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable pulse insights."""
    return f"Pulse Insights: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
