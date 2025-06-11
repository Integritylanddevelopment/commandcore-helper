from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "launch_planner",
    "style": "structured",
    "system_prompt": (
        "You are a launch planner bot. Your task is to orchestrate go-to-market strategies with timelines, messaging milestones, "
        "campaign phases, and multi-channel coordination plans."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract campaign details
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured launch plan output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract campaign details and format them for launch planning."""
    # Example preprocessing logic
    return f"Campaign details: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured launch plan document."""
    # Example postprocessing logic
    return f"### Launch Plan\n{result.strip()}"
