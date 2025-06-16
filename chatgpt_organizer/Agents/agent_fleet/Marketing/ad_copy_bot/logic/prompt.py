import openai


def run_prompt(input_text, platform, audience):
    """Process input for Ad Copy generation with OpenAI assistance."""
    system_prompt = (
        "You are a world-class ad copywriter. Generate creative and high-conversion ad copy "
        "tailored for the specified platform and audience."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Generate ad copy for the following input:\n"
                    f"Platform: {platform}\n"
                    f"Audience: {audience}\n"
                    f"Details: {input_text}"
                ),
            },
        ],
    )

    return response.choices[0].message["content"]


def generate_ad_copy(input_data):
    """Generate ad copy based on input data."""
    ad_request = input_data.get("ad_request", {})
    product = ad_request.get("product", "Unknown Product")
    target_audience = ad_request.get("target_audience", "General Audience")
    key_features = ad_request.get("key_features", [])

    headline = f"Discover {product} – Perfect for {target_audience}!"
    body = (
        f"{product} is designed with {', '.join(key_features)}. "
        "Join the movement towards sustainability and style."
    )
    call_to_action = "Order now and make a difference!"

    return {
        "ad_copy": {
            "headline": headline,
            "body": body,
            "call_to_action": call_to_action
        }
    }
