from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "feature_spec_bot",
    "style": "structured",
    "system_prompt": (
        "You are a feature specification bot. Your task is to convert raw ideas, product thoughts, or problem statements "
        "into fully structured feature specification documents. Include use cases, acceptance criteria, and design notes."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract key ideas
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract key ideas and format them for feature specification."""
    # Example preprocessing logic
    return f"Extracted ideas: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured feature specification document."""
    # Example postprocessing logic
    return f"### Feature Specification\n{result.strip()}"
