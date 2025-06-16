import os
import json

def update_registry():
    """Update the memory agent registry JSON with all agents in the memory/_memory_agents folder."""

    # Current script location
    current_dir = os.path.dirname(__file__)

    # Path to registry.json (beside this script)
    registry_path = os.path.join(current_dir, 'memory_agent_registry.json')

    # Path to _memory_agents folder (one level up)
    memory_agents = os.path.abspath(os.path.join(current_dir, '..'))

    # Initialize registry
    registry = {}

    # Scan the agents folder
    for agent_name in os.listdir(memory_agents):
        agent_path = os.path.join(memory_agents, agent_name)
        if os.path.isdir(agent_path):
            agent_file = os.path.join(agent_path, f"{agent_name}.py")
            meta_file = os.path.join(agent_path, f"{agent_name}.meta.json")

            if os.path.exists(agent_file) and os.path.exists(meta_file):
                with open(meta_file, 'r', encoding='utf-8') as meta:
                    meta_data = json.load(meta)

                registry[agent_name] = {
                    "path": os.path.relpath(agent_file, current_dir).replace('\\', '/'),
                    "meta": os.path.relpath(meta_file, current_dir).replace('\\', '/'),
                    "description": meta_data.get("description", "No description available.")
                }
            else:
                # Print missing or invalid agents
                if not os.path.exists(agent_file):
                    print(f"Missing .py file for agent: {agent_name} ({agent_file})")
                if not os.path.exists(meta_file):
                    print(f"Missing .meta.json file for agent: {agent_name} ({meta_file})")

    with open(registry_path, 'w', encoding='utf-8') as registry_file:
        json.dump(registry, registry_file, indent=2)

    print(f"Registry updated successfully. Total agents: {len(registry)}")

if __name__ == "__main__":
    update_registry()
