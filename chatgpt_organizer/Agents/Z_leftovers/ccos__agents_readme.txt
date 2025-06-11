CommandCoreOS Agent Fleet

This folder contains the full suite of AI agents powering CommandCoreOS. Each agent is a modular intelligence unit designed to handle a specific operational, creative, or strategic task across product, engineering, marketing, support, legal, HR, and admin functions.

ARCHITECTURE
All agents in this directory now include:

- Metadata: Name, role, version, and description
- Structured Schema: Defined input and output JSON schemas
- Core Logic: Custom behavior through a `.run()` method
- Auto Scheduling: Periodic execution via `auto_schedule()`
- Message Hooks: Reactions to intent-labeled messages
- Webhook Handling: API-style external triggers
- Training Data: Self-declared examples for LLM fine-tuning
- Upgrader Injection: Each agent is enhanced dynamically via `core/upgrader.py`
- Agent Registration: Centralized via `registry/agent_registry.py`

INVOCATION FLOW
agent = get_agent("agent_name")
agent = inject(agent)  # Enhances agent before execution
result = agent.run(context)

DIRECTORY STRUCTURE
agents/
├── agent_core.py           # Base class shared by all agents
├── roadmap_bot.py          # Strategic planner for roadmaps
├── ad_copy_bot.py          # Generates high-conversion ad copy
├── admin_assistant.py      # Handles tasks, meetings, reminders
├── ...                     # 50+ total agents

FILE NAMING
snake_case_role_or_function_bot.py

MAINTAINER
This fleet is maintained by the CommandCore Intelligence Team.
