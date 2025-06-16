from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "value_prop_bot",
    "style": "structured",
    "system_prompt": (
        "You are a value proposition bot. Your task is to refine the product's value proposition by breaking down its unique benefits, "
        "target personas, and use cases. Improve positioning through iterative refinement."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Extract product details and format them for value proposition refinement."""
    return f"Product details: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured value proposition document."""
    return f"### Value Proposition\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
