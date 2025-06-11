from agent_core import run_agent

AGENT_CONFIG = {
    "agent_id": "funnel_debugger",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for funnel_debugger."
}

def run(prompt: str):
    return run_agent(prompt, AGENT_CONFIG)
