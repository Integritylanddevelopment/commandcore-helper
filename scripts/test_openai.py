import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not client.api_key:
    print("❌ OPENAI_API_KEY not set in your .env file.")
    exit()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is CommandCore?"}
    ]
)

print("✅ OpenAI Response:")
print(response.choices[0].message.content)
