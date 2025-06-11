from chatgpt_organizer.Agents.agent_fleet.ad_copy_bot.logic import run as ad_copy
from chatgpt_organizer.Agents.agent_fleet.ux_writer.logic.ux_writer import run as ux_writer
from chatgpt_organizer.Agents.agent_fleet.value_prop_bot.logic.value_prop_bot import run as value_prop_bot
from chatgpt_organizer.Agents.agent_fleet.feature_spec_bot.logic.feature_spec_bot import run as feature_spec_bot
from chatgpt_organizer.Agents.agent_fleet.roadmap_bot.logic.roadmap_bot import run as roadmap_bot
from chatgpt_organizer.Agents.agent_fleet.launch_planner.logic.launch_planner import run as launch_planner

# Define a registry of agents and their capabilities
def get_agent(name):
    agents = {
        "ad_copy_bot": ad_copy,
        "ux_writer": ux_writer,
        "value_prop_bot": value_prop_bot,
        "feature_spec_bot": feature_spec_bot,
        "roadmap_bot": roadmap_bot,
        "launch_planner": launch_planner,
        # Add more agents here
    }
    return agents.get(name)

# Define workflows for handoff chains
def define_workflow(agent_chain):
    """
    Define a workflow where tasks are handed off between agents.
    :param agent_chain: List of agent names in the order of execution.
    :return: Function to execute the workflow.
    """
    def workflow(input_data):
        data = input_data
        for agent_name in agent_chain:
            agent = get_agent(agent_name)
            if agent:
                data = agent(data)  # Pass data to the next agent
            else:
                raise ValueError(f"Agent {agent_name} not found in registry.")
        return data

    return workflow

# Example workflows
product_workflow = define_workflow(["value_prop_bot", "feature_spec_bot", "roadmap_bot"])
launch_workflow = define_workflow(["roadmap_bot", "launch_planner"])

# Add more workflows as needed

# Query compatible agents for collaboration
def find_compatible_agents(task_type):
    """
    Find agents compatible with a given task type.
    :param task_type: Type of task to find compatible agents for.
    :return: List of agent names.
    """
    compatibility_map = {
        "copywriting": ["ad_copy_bot", "ux_writer"],
        "product_development": ["value_prop_bot", "feature_spec_bot", "roadmap_bot"],
        "launch_planning": ["launch_planner"],
        # Add more task types and compatible agents
    }
    return compatibility_map.get(task_type, [])

# Log handoff chains
def log_handoff_chain(agent_chain):
    """
    Log the sequence of tasks and agents involved in a workflow.
    :param agent_chain: List of agent names in the order of execution.
    """
    with open("handoff_chain.log", "a") as log_file:
        log_file.write(f"Workflow executed with agents: {', '.join(agent_chain)}\n")
