from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "qa_bot",
    "style": "structured",
    "system_prompt": (
        "You are a QA bot. Your task is to draft robust test cases, perform feature validation logic, and ensure new changes "
        "don’t break existing functionality using comprehensive automated QA workflows."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Extract testing requirements and format them for QA analysis."""
    return f"Testing requirements: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into structured QA output."""
    return f"### QA Output\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
