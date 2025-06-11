def run_prompt(input_text):
    """Process input for Eng Feedback."""
    feedback_data = input_text.get("feedback", [])
    summary = {
        "high_priority": [item for item in feedback_data if item["priority"] == "High"],
        "medium_priority": [item for item in feedback_data if item["priority"] == "Medium"]
    }
    recommendations = [
        "Optimize the CI/CD pipeline to improve build speed.",
        "Update the API documentation to reflect recent changes."
    ]
    return {
        "summary": summary,
        "recommendations": recommendations
    }
