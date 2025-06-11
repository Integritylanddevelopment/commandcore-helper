from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "compliance_checker",
    "style": "structured",
    "system_prompt": (
        "You are a compliance checker bot. Your task is to analyze documents and processes to ensure compliance with relevant "
        "regulations and standards."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for compliance analysis."""
    return f"Compliance context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable compliance recommendations."""
    return f"Compliance Recommendations: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
