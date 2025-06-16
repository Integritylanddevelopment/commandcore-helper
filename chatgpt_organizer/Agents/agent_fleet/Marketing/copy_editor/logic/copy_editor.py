from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "copy_editor",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for copy_editor."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
