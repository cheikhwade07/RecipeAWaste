import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Read API key from environment variable for safety
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
  raise RuntimeError("Environment variable GROQ_API_KEY is not set. Set it before running the script.")

client = Groq(api_key=api_key)
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": "From this ingredient list in my fridge, choose some and make a recipe:\nApples : 3\nMandarine : 10\nChicken breast : 5\nsoya milk : 1L\n"
      }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

for chunk in completion:
  print(chunk.choices[0].delta.content or "", end="")
