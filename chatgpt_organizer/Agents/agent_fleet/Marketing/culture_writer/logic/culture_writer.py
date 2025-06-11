from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "culture_writer",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for culture_writer."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
