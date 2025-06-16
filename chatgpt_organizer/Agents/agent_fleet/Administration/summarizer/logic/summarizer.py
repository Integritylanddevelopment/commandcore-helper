from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "summarizer",
    "style": "structured",
    "system_prompt": (
        "You are a summarizer bot. Your task is to condense lengthy content into concise and informative summaries. "
        "Ensure the key points are captured accurately and presented clearly."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for summarization."""
    return f"Content to summarize: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured summary."""
    return f"### Summary\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
