from chatgpt_organizer.utils.agent_utils import run_agent

def test_run_agent():
    config = {"agent_id": "test_agent"}
    result = run_agent("Test prompt", config)
    print("Result:", result)

if __name__ == "__main__":
    test_run_agent()
