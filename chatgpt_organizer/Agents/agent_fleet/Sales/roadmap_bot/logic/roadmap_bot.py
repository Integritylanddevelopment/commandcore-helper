from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "roadmap_bot",
    "style": "structured",
    "system_prompt": (
        "You are a roadmap bot. Your task is to cluster related product initiatives into thematic roadmaps, prioritize them "
        "based on business goals and effort vs. impact analysis, and suggest sequencing for execution."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Extract product initiatives and format them for roadmap analysis."""
    return f"Roadmap context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into structured roadmap output."""
    return f"### Roadmap\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
