# chatgpt_organizer/agents/assistant_sync.py

import os
import openai
import logging
from dotenv import load_dotenv
from pathlib import Path
from agent_core import upgrade_agent_core, train_llm
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_PATH = Path("data/organized")


def pull_assistant_chat(thread_id, project_name="gpt_imports", chat_name="chat_from_gpt", retries=3):
    """
    Pull assistant chat thread and save locally.
    Includes retry logic for failed API calls.
    """
    attempt = 0
    while attempt < retries:
        try:
            if not thread_id or not openai.api_key:
                logging.error("Missing thread_id or API key.")
                return

            logging.info(f"Pulling thread: {thread_id} (Attempt {attempt + 1})")
            response = openai.beta.threads.messages.list(thread_id=thread_id)
            messages = response.data[::-1]  # most recent last

            folder = DATA_PATH / project_name / chat_name
            folder.mkdir(parents=True, exist_ok=True)

            out_path = folder / "chat.md"
            with open(out_path, "w", encoding="utf-8") as f:
                for msg in messages:
                    role = msg.role.upper()
                    timestamp = msg.created_at
                    content = msg.content[0].text.value.strip()
                    f.write(f"**{role}** ({timestamp}):\n{content}\n\n")

            logging.info(f"Chat saved to: {out_path}")

            # Simulate saving messages
            logging.info(f"Saving messages to {DATA_PATH / project_name / chat_name}.json")
            upgrade_agent_core()  # Upgrade the agent core after synchronization
            train_llm()  # Train the LLM after synchronization
            logging.info("Synchronization complete.")
            return
        except Exception as e:
            logging.error(f"Error during synchronization: {e}")
            attempt += 1
            time.sleep(2)  # Wait before retrying

    logging.error("Failed to synchronize after multiple attempts.")


def upgrade_self():
    try:
        logging.info("Upgrading assistant_sync bot...")
        # Simulate upgrade logic
        logging.info("assistant_sync bot upgrade complete.")
    except Exception as e:
        logging.error(f"Error during upgrade: {e}")
        raise


def pull_multiple_threads(thread_ids, project_name="gpt_imports"):
    """
    Synchronize multiple threads in a single invocation.
    """
    for thread_id in thread_ids:
        chat_name = f"chat_{thread_id}"
        pull_assistant_chat(thread_id, project_name, chat_name)


def categorize_messages(messages):
    """
    Categorize messages based on roles.
    """
    categorized = {}
    for msg in messages:
        role = msg.role.upper()
        if role not in categorized:
            categorized[role] = []
        categorized[role].append(msg.content[0].text.value.strip())
    return categorized


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--thread", required=True, help="OpenAI thread_id to sync")
    parser.add_argument("--project", default="gpt_imports")
    parser.add_argument("--chat", default="chat_from_gpt")
    args = parser.parse_args()

    pull_assistant_chat(args.thread, args.project, args.chat)
