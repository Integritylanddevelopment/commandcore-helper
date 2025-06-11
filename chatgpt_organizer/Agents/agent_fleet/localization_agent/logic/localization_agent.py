from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "localization_agent",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for localization_agent."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
