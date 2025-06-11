from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "bug_reporter",
    "style": "structured",
    "system_prompt": (
        "You are a bug reporter bot. Your task is to capture and reformat bug issues into clear, reproducible reports with environment details, "
        "steps to replicate, and system logs to assist the development team."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract bug details
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured bug report output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract bug details and format them for reporting."""
    # Example preprocessing logic
    return f"Bug details: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured bug report document."""
    # Example postprocessing logic
    return f"### Bug Report\n{result.strip()}"
