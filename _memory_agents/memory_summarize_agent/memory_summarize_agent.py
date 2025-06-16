import os
from datetime import datetime
import openai

def summarize(filepath: str) -> str:
    """Summarize the content of a file using OpenAI GPT."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # OpenAI API call
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize this content clearly in markdown bullet points:\n{content}",
            max_tokens=500
        )

        summary = response.choices[0].text.strip()

        # Log the summary action
        log_path = os.path.join(os.path.dirname(__file__), '../logs/summarize_agent_log.md')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"[{datetime.now()}] Summarized file: {filepath}\n")

        return summary

    except Exception as e:
        return f"Error summarizing file: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(summarize(filepath))
    else:
        print("Usage: python summarize_agent.py path/to/file.md")
