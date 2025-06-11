from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "email_split_bot",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for email_split_bot."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
