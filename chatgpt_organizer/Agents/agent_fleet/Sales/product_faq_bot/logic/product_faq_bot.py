from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "product_faq_bot",
    "style": "structured",
    "system_prompt": (
        "You are a product FAQ bot. Your task is to extract commonly asked questions from support tickets, internal docs, and Slack threads, "
        "turning them into structured FAQ entries that can be embedded into help centers or product guides."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract FAQ details
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured FAQ output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract FAQ details and format them for documentation."""
    # Example preprocessing logic
    return f"FAQ details: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured FAQ document."""
    # Example postprocessing logic
    return f"### Product FAQ\n{result.strip()}"
