import openai


def run_prompt(input_text):
    """Process input for Admin Assistant."""
    # OpenAI API call to process the input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an admin assistant bot."},
            {"role": "user", "content": input_text},
        ],
    )
    return response["choices"][0]["message"]["content"]
