from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "inbox_responder",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for inbox_responder."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
