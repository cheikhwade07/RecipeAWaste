from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os

from pyasn1_modules.rfc2315 import data

from fridge import Fridge
from src.food_item import FoodItem

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
fridge = Fridge()

@app.post("/generate")
async def generate_recipe():
    ingredients = fridge.get_all_items()

    # Format ingredients
    ingredients_text = "\n".join([
        f"{item.name}: Calories {item.calorie}, Protein {item.protein}g"
        for item in ingredients
    ])

    # Call Groq API
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"Create a recipe using these ingredients:\n{ingredients_text}"
        }],
        temperature=0.7,
        max_tokens=2000,
    )

    return completion.choices[0].message.content
@app.post("/add_Food_Item")
def add_food_item(data: dict):  # Fix: accept data parameter
    name = data.get("name")
    calorie = data.get("calorie", 0)
    protein = data.get("protein", 0)
    expiry_date = data.get("expiry_date")

    foodItem = FoodItem(name, calorie, protein, expiry_date)
    fridge.add_item(foodItem)
    return {"message": "Added to fridge"}

@app.delete("/remove_Food_Item")
def remove_food_item(name: str)->None :
    fridge.remove_item(name)
    return {"message": name +" removed to fridge"}

@app.delete("/clear_Fridge")
def remove_food_item()->None :
    fridge.clear()
    return {"message":"Fridge cleared"}
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)