from agent_core import run_agent, upgrade_agent_core, train_llm
from chatgpt_organizer.utils.agent_utils import batch_and_throttle_requests
import logging
import openai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AGENT_CONFIG = {
    "agent_id": "brand_story_bot",
    "style": "auto-generated",
    "system_prompt": "Placeholder system prompt for brand_story_bot."
}

def run(prompt: str):
    try:
        logging.info(f"Running brand story generation task with prompt: {prompt}")
        result = run_agent(prompt, AGENT_CONFIG)
        upgrade_agent_core()  # Upgrade the agent core after running a task
        train_llm()  # Train the LLM after running a task
        logging.info("Brand story generation task completed successfully.")
        return result
    except Exception as e:
        logging.error(f"Error during brand story generation task execution: {e}")
        raise

def upgrade_self():
    try:
        logging.info("Upgrading brand_story_bot...")
        # Simulate upgrade logic
        logging.info("brand_story_bot upgrade complete.")
    except Exception as e:
        logging.error(f"Error during upgrade: {e}")
        raise

def generate_story(audience: str, values: list):
    try:
        logging.info(f"Generating brand story for audience: {audience} with values: {values}")
        # Simulate story generation logic
        logging.info("Brand story generated successfully.")
    except Exception as e:
        logging.error(f"Error during brand story generation: {e}")
        raise

def generate_brand_story(prompt: str):
    logging.info(f"Generating brand story with prompt: {prompt}")

    try:
        response = batch_and_throttle_requests(
            lambda: openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": AGENT_CONFIG["system_prompt"]},
                    {"role": "user", "content": prompt}
                ]
            )
        )
        logging.info("OpenAI Response:", response)
    except Exception as e:
        logging.error(f"Error during OpenAI API call: {e}")

    return response
