from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "onboarding_coach",
    "style": "structured",
    "system_prompt": (
        "You are an onboarding coach bot. Your task is to create step-by-step onboarding documentation, checklists, role-specific flows, "
        "and milestone guides to help new users or employees understand and engage with the product quickly."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Extract onboarding details and format them for onboarding analysis."""
    return f"Onboarding context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into structured onboarding output."""
    return f"### Onboarding Documentation\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
