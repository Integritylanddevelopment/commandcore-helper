import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'chatgpt_organizer')))

from chatgpt_organizer.utils.agent_utils import batch_and_throttle_requests
from chatgpt_organizer.Agents.agent_registry import product_workflow, launch_workflow

def test_workflows():
    input_data = {"key": "value"}  # Example input data

    # Test product workflow
    try:
        product_result = product_workflow(input_data)
        print("Product workflow executed successfully:", product_result)
    except Exception as e:
        print("Product workflow failed:", e)

    # Test launch workflow
    try:
        launch_result = launch_workflow(input_data)
        print("Launch workflow executed successfully:", launch_result)
    except Exception as e:
        print("Launch workflow failed:", e)

    # Test batching and throttling
    input_prompts = [
        "Create a feature spec for a new app.",
        "Generate a roadmap for product launch.",
        "Refine the value proposition for a SaaS product.",
        "Plan the launch strategy for a new product."
    ]

    config = {"agent_id": "test_agent", "system_prompt": "Test system prompt."}

    try:
        results = batch_and_throttle_requests(input_prompts, config, delay=1.0)
        print("Batch results:", results)
    except Exception as e:
        print("Batch execution failed:", e)

if __name__ == "__main__":
    test_workflows()
