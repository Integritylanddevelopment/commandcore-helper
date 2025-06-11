# agent_core.py

from typing import Dict, Any
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from chatgpt_organizer.Agents.agent_registry import get_agent
from chatgpt_organizer.Agents.agent_fleet.ad_copy_bot.logic import run as ad_copy_bot_run
from chatgpt_organizer.Agents.agent_fleet.value_prop_bot.logic.value_prop_bot import run as value_prop_bot_run
from chatgpt_organizer.Agents.agent_fleet.feature_spec_bot.logic.feature_spec_bot import run as feature_spec_bot_run
from chatgpt_organizer.Agents.agent_fleet.roadmap_bot.logic.roadmap_bot import run as roadmap_bot_run
from chatgpt_organizer.Agents.agent_fleet.launch_planner.logic.launch_planner import run as launch_planner_run
from chatgpt_organizer.utils.agent_utils import run_agent

class AgentCore:
    def __init__(self, name: str):
        self.name = name
        self.memory = {}

    def inject_memory(self, context: Dict[str, Any]):
        # Simulated dynamic context expansion
        self.memory.update(context)

    def route(self, context: Dict[str, Any]):
        """Route context to appropriate logic module or agent."""
        agent_name = context.get("target_agent")
        if not agent_name:
            return {"error": "No target_agent specified"}

        # Routing logic for ad copy bot
        if agent_name == "ad_copy_bot":
            return ad_copy_bot_run(context)

        # Routing logic for product development bots
        if agent_name == "feature_spec_bot":
            return feature_spec_bot_run(context)
        elif agent_name == "roadmap_bot":
            return roadmap_bot_run(context)
        elif agent_name == "value_prop_bot":
            return value_prop_bot_run(context)
        elif agent_name == "launch_planner":
            return launch_planner_run(context)

        # Default routing using agent registry
        agent = get_agent(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} not found"}

        return agent.run(context)

    def sync(self):
        # Placeholder for shared memory sync logic
        print("Memory synced across fleet")

    def run(self, context: Dict[str, Any]):
        self.inject_memory(context)
        result = self.route(context)
        self.sync()
        return result
