from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "finance_bot",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for finance_bot."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
