from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "funding_advisor",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for funding_advisor."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
