import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
if api_key==None:
    raise RuntimeError("Environment variable GROQ_API_KEY is not set. Set it before running the script.")

client = Groq(api_key=api_key)


completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "From this ingredient list in my fridge, choose some and make a recipe:\nApples: 3\nMandarine: 10\nChicken breast: 5\nSoya milk: 1L\n"
        }
    ],
    temperature=0.7,
    max_tokens=2000,
    top_p=1,
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

print()