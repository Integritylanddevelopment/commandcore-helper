from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "note_taker",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for note_taker."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
