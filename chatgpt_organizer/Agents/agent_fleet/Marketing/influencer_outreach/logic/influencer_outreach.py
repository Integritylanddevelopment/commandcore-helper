from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests

AGENT_CONFIG = {
    "agent_id": "influencer_outreach",
    "style": "structured",
    "system_prompt": (
        "You are an influencer outreach bot. Your task is to identify and engage with influencers who align with the brand's values. "
        "Focus on crafting personalized outreach messages and building long-term partnerships."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for influencer outreach analysis."""
    return f"Outreach context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable outreach strategies."""
    return f"### Outreach Strategies\n{result.strip()}"

def run(prompt: str):
    # Preprocess the input prompt
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic with batching and throttling
    result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))

    # Postprocess the result
    return postprocess_result(result)
