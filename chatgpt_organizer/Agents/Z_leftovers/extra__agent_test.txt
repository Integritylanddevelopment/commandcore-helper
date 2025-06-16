# agents/agent_test.py

"""
Unit test stub for agent functionality and schema integrity.
"""

import unittest
from agents.roadmap_bot import RoadmapBot

class TestAgents(unittest.TestCase):
    def test_roadmap_bot_run(self):
        agent = RoadmapBot()
        context = {
            "project_phase": "MVP",
            "key_goals": ["Launch beta"],
            "constraints": ["Limited time"]
        }
        result = agent.run(context)
        self.assertIn("milestones", result)

if __name__ == "__main__":
    unittest.main()
