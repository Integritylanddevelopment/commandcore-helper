from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "ui_evaluator",
    "style": "structured",
    "system_prompt": (
        "You are a UI evaluator bot. Your task is to assess user interfaces for usability, accessibility, and design consistency. "
        "Provide actionable feedback to improve the overall user experience."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for UI evaluation."""
    return f"UI evaluation context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable UI evaluation feedback."""
    return f"### UI Evaluation Feedback\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
