import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'chatgpt_organizer')))

try:
    from Agents.agent_fleet.ad_copy_bot.logic import run as ad_copy_bot_run
    print("Import successful!")
except ModuleNotFoundError as e:
    print(f"Import failed: {e}")
