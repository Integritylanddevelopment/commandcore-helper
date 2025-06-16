from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AGENT_CONFIG = {
    "agent_id": "branding_coach",
    "style": "structured",
    "system_prompt": (
        "You are a branding coach bot. Your task is to analyze brand identity and provide actionable recommendations to enhance "
        "brand consistency, messaging, and market positioning."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for branding analysis."""
    return f"Branding context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable branding recommendations."""
    return f"### Branding Recommendations\n{result.strip()}"

def run(prompt: str):
    try:
        logging.info(f"Running branding analysis task with prompt: {prompt}")
        processed_prompt = preprocess_prompt(prompt)
        result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))
        logging.info("Branding analysis task completed successfully.")
        return postprocess_result(result)
    except Exception as e:
        logging.error(f"Error during branding analysis task: {e}")
        raise
