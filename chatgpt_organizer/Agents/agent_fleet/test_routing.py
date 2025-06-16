import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'chatgpt_organizer')))

from chatgpt_organizer.Agents.agent_core.core_logic.logic.agent_core import AgentCore

def test_routing():
    agent_core = AgentCore(name="TestAgentCore")

    # Test ad_copy_bot routing
    ad_copy_context = {"target_agent": "ad_copy_bot", "prompt": "Write ad copy for a new product."}
    ad_copy_result = agent_core.run(ad_copy_context)
    print("ad_copy_bot result:", ad_copy_result)

    # Test feature_spec_bot routing
    feature_spec_context = {"target_agent": "feature_spec_bot", "prompt": "Create a feature spec for a new app."}
    feature_spec_result = agent_core.run(feature_spec_context)
    print("feature_spec_bot result:", feature_spec_result)

    # Test roadmap_bot routing
    roadmap_context = {"target_agent": "roadmap_bot", "prompt": "Generate a roadmap for product launch."}
    roadmap_result = agent_core.run(roadmap_context)
    print("roadmap_bot result:", roadmap_result)

    # Test value_prop_bot routing
    value_prop_context = {"target_agent": "value_prop_bot", "prompt": "Refine the value proposition for a SaaS product."}
    value_prop_result = agent_core.run(value_prop_context)
    print("value_prop_bot result:", value_prop_result)

    # Test launch_planner routing
    launch_planner_context = {"target_agent": "launch_planner", "prompt": "Plan the launch strategy for a new product."}
    launch_planner_result = agent_core.run(launch_planner_context)
    print("launch_planner result:", launch_planner_result)

if __name__ == "__main__":
    test_routing()
