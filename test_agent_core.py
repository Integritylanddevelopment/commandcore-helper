import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'chatgpt_organizer')))

from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_core import AgentCore

def test_agent_core():
    agent_core = AgentCore(name="TestAgentCore")
    print("AgentCore initialized successfully.")

if __name__ == "__main__":
    test_agent_core()
