from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_utils import run_agent

AGENT_CONFIG = {
    "agent_id": "deployment_planner",
    "style": "structured",
    "system_prompt": (
        "You are a deployment planner bot. Your task is to design detailed rollout strategies, rollback contingencies, "
        "and phased deployment plans to ensure smooth product updates with minimal risk."
    ),
    "output_format": "markdown",
}

def run(prompt: str):
    # Preprocess the input prompt to extract deployment details
    processed_prompt = preprocess_prompt(prompt)

    # Execute the agent logic
    result = run_agent(processed_prompt, AGENT_CONFIG)

    # Postprocess the result to ensure structured deployment plan output
    return postprocess_result(result)

def preprocess_prompt(prompt: str) -> str:
    """Extract deployment details and format them for planning."""
    # Example preprocessing logic
    return f"Deployment details: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into a structured deployment plan document."""
    # Example postprocessing logic
    return f"### Deployment Plan\n{result.strip()}"
