import json
from assistant_sync import pull_assistant_chat
from pathlib import Path

# Load example inputs
example_inputs_path = Path(__file__).parent / "example_inputs.json"
with open(example_inputs_path, "r") as f:
    inputs = json.load(f)

# Test the assistant_sync functionality
try:
    pull_assistant_chat(
        thread_id=inputs["thread_id"],
        project_name=inputs["project_name"],
        chat_name=inputs["chat_name"]
    )
    print("Test completed successfully.")
except Exception as e:
    print(f"Test failed: {e}")
