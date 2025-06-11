# logic/test_agent.py

from typing import Dict

class TestAgent:
    def run(self, context: Dict) -> Dict:
        return {
            "status": "success",
            "echo": context
        }
