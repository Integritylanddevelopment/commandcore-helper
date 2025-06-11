from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AGENT_CONFIG = {
    "agent_id": "api_doc_bot",
    "style": "structured",
    "system_prompt": (
        "You are an API documentation bot. Your task is to generate and maintain comprehensive API documentation, "
        "including usage examples, parameter descriptions, and integration guides."
    ),
    "output_format": "markdown",
}

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for API documentation."""
    return f"API documentation context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into structured API documentation."""
    return f"### API Documentation\n{result.strip()}"

def run(prompt: str):
    try:
        logging.info(f"Running API documentation task with prompt: {prompt}")
        processed_prompt = preprocess_prompt(prompt)
        result = batch_and_throttle_requests(lambda: run_agent(processed_prompt, AGENT_CONFIG))
        logging.info("API documentation task completed successfully.")
        return postprocess_result(result)
    except Exception as e:
        logging.error(f"Error during API documentation task: {e}")
        raise
