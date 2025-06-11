
# agents/roadmap_bot.py

"""
Agent Name: roadmap_bot
Role: Planner
Version: 1.0.0
Description: Generates detailed project roadmaps based on the project phase, user goals, constraints, and system state.
"""

import json
import datetime
from agents.agent_core import BaseAgent
from utils.roadmap_generator import generate_roadmap
from core.scheduler import schedule_task
from core.messaging import handle_message
from core.webhooks import register_webhook
from core.training import register_training_example
from registry.agent_registry import register_agent

# Agent Metadata
agent_name = "roadmap_bot"
agent_description = "Generates intelligent project roadmaps from user input, tracking system state and external dependencies."
agent_role = "planner"
agent_version = "1.0.0"

# Expanded Input Schema
expected_input = {
    "project_name": "string",
    "project_phase": "string",
    "key_goals": ["string"],
    "constraints": ["string"],
    "team_members": ["string"],
    "technologies": ["string"],
    "timeline_preference": "string",
    "priority_style": "string"
}

# Expanded Output Schema
output_format = {
    "milestones": ["string"],
    "timeline_estimate": "string",
    "dependency_graph": {"task": ["dependency"]},
    "recommended_tools": ["string"],
    "risk_warnings": ["string"]
}

# Agent Logic
class RoadmapBot(BaseAgent):
    def __init__(self):
        super().__init__(
            name=agent_name,
            description=agent_description,
            role=agent_role,
            version=agent_version,
            input_schema=expected_input,
            output_schema=output_format
        )

    def run(self, context):
        try:
            roadmap = generate_roadmap(context)
            self.log("Roadmap generated successfully")
            return roadmap
        except Exception as e:
            self.error(f"Roadmap generation failed: {str(e)}")
            return {"error": str(e)}

    def auto_schedule(self):
        schedule_task(agent_name, self.run, day_of_week="mon", hour=9)

    def message_hooks(self, message_data):
        if "roadmap" in message_data.get("intent", ""):
            return self.run(message_data.get("context", {}))
        return {"status": "ignored"}

    def webhook_handler(self, payload):
        project_data = payload.get("project_context", {})
        return self.run(project_data)

    def training_data(self):
        examples = [
            {
                "input": {
                    "project_name": "TogetherWe App",
                    "project_phase": "MVP",
                    "key_goals": ["Launch beta", "Set up Stripe"],
                    "constraints": ["2-week timeline", "limited dev help"],
                    "technologies": ["Firebase", "React Native"],
                    "priority_style": "speed"
                },
                "output": {
                    "milestones": ["Setup Firebase", "Configure auth", "Implement Stripe checkout"],
                    "timeline_estimate": "2 weeks",
                    "dependency_graph": {
                        "Configure auth": ["Setup Firebase"],
                        "Implement Stripe checkout": ["Configure auth"]
                    },
                    "recommended_tools": ["Firebase Auth", "Stripe Elements"],
                    "risk_warnings": ["Solo dev may delay backend"]
                }
            }
        ]
        for example in examples:
            register_training_example(agent_name, example["input"], example["output"])

# Agent Registration
register_agent(RoadmapBot)

# Dev Test Stub
if __name__ == "__main__":
    test_context = {
        "project_name": "TogetherWe MVP",
        "project_phase": "MVP",
        "key_goals": ["Launch beta", "Set up payments"],
        "constraints": ["Solo dev", "2-week timeline"],
        "team_members": ["alex"],
        "technologies": ["Firebase", "Stripe"],
        "timeline_preference": "14 days",
        "priority_style": "speed"
    }

    bot = RoadmapBot()
    output = bot.run(test_context)
    print(json.dumps(output, indent=2))
