# logic/__init__.py

from typing import Dict

def run(context: Dict) -> Dict:
    """
    Generates high-conversion ad copy based on input context.
    
    Args:
        context (dict): {
            "product_name": str,
            "description": str,
            "target_audience": str,
            "platform": str  # e.g., "Facebook", "Google", "TikTok"
        }

    Returns:
        dict: {
            "headline": str,
            "body": str,
            "cta": str
        }
    """
    product = context.get("product_name", "your product")
    description = context.get("description", "")
    audience = context.get("target_audience", "everyone")
    platform = context.get("platform", "generic")

    headline = f"Discover {product} — Perfect for {audience}!"
    body = f"{description} Try {product} today and see the difference."
    cta = "Learn More" if platform.lower() == "google" else "Shop Now"

    return {
        "headline": headline,
        "body": body,
        "cta": cta
    }

def auto_schedule():
    # Placeholder for future timed tasks, e.g., weekly campaign refresh
    pass
