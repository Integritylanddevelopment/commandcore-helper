import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_search_query():
    """Run the search query script."""
    try:
        logging.info("Starting: Search Memory (Whoosh)")
        subprocess.run(["python", "memory/memory_sys_scripts/search_index_whoosh.py"], check=True)
        logging.info("Completed: Search Memory (Whoosh)")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed: Search Memory (Whoosh) with error: {e}")
        raise

if __name__ == "__main__":
    run_search_query()
