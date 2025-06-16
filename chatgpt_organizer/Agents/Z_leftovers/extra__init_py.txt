# agents/__init__.py

"""
Auto-imports all agents in the directory for dynamic registration.
This file ensures the 'agents' folder behaves as a Python module.
"""

from agents.agent_core import BaseAgent
# Agents will register themselves via register_agent() upon import
