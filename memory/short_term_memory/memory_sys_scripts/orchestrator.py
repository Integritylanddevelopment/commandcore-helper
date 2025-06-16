import subprocess
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_path, description):
    """Run a script and log its status."""
    try:
        logging.info(f"Starting: {description}")
        subprocess.run(["python", script_path], check=True)
        logging.info(f"Completed: {description}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed: {description} with error: {e}")
        raise

def update_readme_with_schema():
    schema_content = """
    ## Schema Overview

    The CommandCore Hub schema is designed to provide a structured and scalable approach to data management. Below is an overview of the schema:

    ### Entities

    - **Users**: Information about users, including roles and permissions.
    - **Projects**: Details about projects, including timelines and deliverables.
    - **Tasks**: Specific tasks associated with projects, including status and priority.
    - **Logs**: Comprehensive logs for tracking activities and changes.

    ### Relationships

    - **User-Project**: Users can be assigned to multiple projects.
    - **Project-Task**: Each project can have multiple tasks.
    - **Task-Log**: Each task can generate multiple logs.

    ### Attributes

    - **User Attributes**: Name, email, role.
    - **Project Attributes**: Title, description, start date, end date.
    - **Task Attributes**: Title, description, status, priority.
    - **Log Attributes**: Timestamp, action, details.
    """

    readme_path = "d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\README_Project_Overview.md"

    with open(readme_path, "a") as readme_file:
        readme_file.write(schema_content)

def update_readme():
    additional_content = """
    ## Additional Information

    CommandCore Hub is actively evolving, and we welcome contributions from developers, researchers, and designers. Join us in building the future of development workflows.

    ### How to Contribute

    - Fork the repository and submit pull requests.
    - Report issues and suggest features.
    - Share your use cases and feedback.

    ### Contact Us

    - **GitHub**: [CommandCore Hub Repository](https://github.com/your-repo/CommandCore-Hub)
    - **Email**: [Your Email](mailto:your-email@example.com)
    """

    readme_path = "d:\\ActiveProjects\\CommandCore-Hub_v2025.01.01\\README_Project_Overview.md"

    with open(readme_path, "a") as readme_file:
        readme_file.write(additional_content)

def main():
    """Coordinate the execution of scripts within the memory system."""
    try:
        # Step 1: Index memory (Whoosh)
        run_script("memory/memory_sys_scripts/index_memory_whoosh.py", "Index Memory (Whoosh)")

        # Step 2: Update session log
        run_script("memory/logs/log_scripts/update_session_log.py", "Update Session Log")

        # Step 3: Summarize sessions
        run_script("memory/summaries/summeries_scripts/summarize_sessions.py", "Summarize Sessions")

        # Step 4: Extract scripts
        run_script("scripts/extract_scripts.py", "Extract Scripts")

        # Step 5: Merge logs
        run_script("memory/logs/merged/merge_scripts/merge_logs.py", "Merge Logs")

        # Update README with schema information
        update_readme_with_schema()

        # Update README with additional information
        update_readme()

        logging.info("Memory system orchestration completed successfully.")
    except Exception as e:
        logging.error(f"Memory system orchestration failed: {e}")

if __name__ == "__main__":
    main()
