import os
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Simple test
response = client.chat.completions.create(
    # model="llama-3.3-70b-versatile",  # Working model
    # model="qwen/qwen3-32b",  # Working model
    # model="meta-llama/llama-4-scout-17b-16e-instruct",  # Working model
    
    messages=[{"role": "user", "content": "Say 'API is working!'"}],
    temperature=0.1,
    max_tokens=20
)

# Print result
print(response.choices[0].message.content)