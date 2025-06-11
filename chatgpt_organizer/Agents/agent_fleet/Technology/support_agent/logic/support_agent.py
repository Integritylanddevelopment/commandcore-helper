from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "support_agent",
    "style": "structured",
    "system_prompt": (
        "You are a support agent bot. Your task is to assist customers by providing accurate and timely responses to their queries. "
        "Analyze the input and generate helpful solutions or escalate issues as needed."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for customer support analysis."""
    return f"Customer query: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable support responses."""
    return f"Support Response: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
