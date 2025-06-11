from typing import Dict

def run_agent(prompt: str, config: Dict):
    """Simulated agent execution logic."""
    return {
        "agent_id": config.get("agent_id"),
        "response": f"Processed prompt: {prompt}"
    }
