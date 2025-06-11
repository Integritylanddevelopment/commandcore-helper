from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "ecommerce_advisor",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for ecommerce_advisor."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
