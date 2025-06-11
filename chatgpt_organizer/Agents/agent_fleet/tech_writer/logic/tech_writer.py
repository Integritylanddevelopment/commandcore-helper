from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "tech_writer",
    "style": "structured",
    "system_prompt": (
        "You are a tech writer bot. Your task is to write and maintain technical documentation, including API references, developer onboarding guides, "
        "backend architecture overviews, and integration manuals."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Extract documentation requirements and format them for technical writing."""
    return f"Documentation context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into structured technical documentation."""
    return f"### Technical Documentation\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
