from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "developer_bot",
    "style": "structured",
    "system_prompt": (
        "You are a developer bot. Your task is to generate or explain full-stack application code in languages like Python, JavaScript, and more. "
        "Support front-end, back-end, and database-level implementations."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract development requirements
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured development output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract development requirements and format them for code generation."""
    # Example preprocessing logic
    return f"Development requirements: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured development document."""
    # Example postprocessing logic
    return f"### Development Output\n{result.strip()}"
