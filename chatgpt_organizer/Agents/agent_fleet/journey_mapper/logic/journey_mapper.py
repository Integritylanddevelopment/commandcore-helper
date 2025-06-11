from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "journey_mapper",
    "style": "structured",
    "system_prompt": (
        "You are a journey mapper bot. Your task is to map end-to-end user flows across the product, identify friction points or drop-offs, "
        "and recommend improvements to ensure seamless customer experience."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract user flow details
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured journey mapping output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract user flow details and format them for journey mapping."""
    # Example preprocessing logic
    return f"User flow details: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured journey mapping document."""
    # Example postprocessing logic
    return f"### Journey Mapping\n{result.strip()}"
