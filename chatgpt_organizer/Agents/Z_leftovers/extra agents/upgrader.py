# core/upgrader.py

"""
Upgrader Module
Purpose: Enhances agent intelligence by injecting new training data and logic upgrades on each run.
"""

from core.training import get_pending_examples
from core.rewrites import suggest_logic_changes

def inject(agent):
    # Inject new fine-tuning data if any
    pending_examples = get_pending_examples(agent.name)
    if pending_examples:
        if hasattr(agent, "training_data") and callable(agent.training_data):
            try:
                current = agent.training_data()
                if isinstance(current, list):
                    current.extend(pending_examples)
                    agent.log(f"Injected {len(pending_examples)} new training examples.")
            except Exception as e:
                agent.error(f"Training data injection failed: {str(e)}")

    # Dynamically suggest and apply logic patches
    logic_patch = suggest_logic_changes(agent)
    if logic_patch and hasattr(agent, "apply_patch"):
        try:
            agent.apply_patch(logic_patch)
            agent.log("Logic patch applied successfully.")
        except Exception as e:
            agent.error(f"Logic patch application failed: {str(e)}")

    return agent
