from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "persona_builder",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for persona_builder."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
