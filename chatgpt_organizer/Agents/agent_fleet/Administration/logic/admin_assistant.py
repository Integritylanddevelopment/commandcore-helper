from chatgpt_organizer.utils.agent_utils import run_agent, batch_and_throttle_requests
import logging
import openai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

AGENT_CONFIG = {
    "agent_id": "admin_assistant",
    "style": "structured",
    "system_prompt": (
        "You are an admin assistant bot. Your task is to manage administrative tasks, including scheduling, document organization, "
        "and communication coordination."
    ),
    "output_format": "json",
}

OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY

def preprocess_prompt(prompt: str) -> str:
    """Format the input prompt for administrative task analysis."""
    return f"Administrative context: {prompt.strip()}"

def postprocess_result(result: str) -> str:
    """Format the result into actionable administrative strategies."""
    return f"Administrative Strategies: {result.strip()}"

def run_openai(prompt: str) -> str:
    """Use OpenAI's GPT models to process the prompt."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error with OpenAI API: {e}")
        raise

def run(prompt: str):
    try:
        logging.info(f"Running administrative task with prompt: {prompt}")
        processed_prompt = preprocess_prompt(prompt)
        openai_result = run_openai(processed_prompt)
        result = batch_and_throttle_requests(lambda: run_agent(openai_result, AGENT_CONFIG))
        logging.info("Administrative task completed successfully.")
        return postprocess_result(result)
    except Exception as e:
        logging.error(f"Error during administrative task: {e}")
        raise
