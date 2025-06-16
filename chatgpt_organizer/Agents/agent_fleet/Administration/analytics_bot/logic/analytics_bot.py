from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AGENT_CONFIG = {
    "agent_id": "analytics_bot",
    "style": "structured",
    "system_prompt": (
        "You are an analytics bot. Your task is to analyze data and provide actionable insights to improve decision-making. "
        "Focus on identifying trends, anomalies, and opportunities."
    ),
    "output_format": "json",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for data analytics."""
    return f"Analytics context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable analytics insights."""
    return f"Analytics Insights: {result.strip()}"

def run(prompt: str):
    try:
        logging.info(f"Running analytics task with prompt: {prompt}")
        processed_prompt = preprocess_prompt(prompt)
        result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))
        logging.info("Analytics task completed successfully.")
        return postprocess_result(result)
    except Exception as e:
        logging.error(f"Error during analytics task: {e}")
        raise
