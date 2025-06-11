from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "ticket_router",
    "style": "structured",
    "system_prompt": (
        "You are a ticket routing bot. Your task is to analyze incoming support tickets and route them to the appropriate team. "
        "Ensure accurate categorization and prioritization based on the ticket content."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for ticket routing analysis."""
    return f"Ticket content: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable routing instructions."""
    return f"Routing Instructions: {result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
