"""
FastAPI backend for RecipeAWaste.
Uses existing FoodItem and Fridge classes without modification.
"""

import os
from datetime import datetime
from typing import List, Optional


from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel
from fridge import Fridge
from food_item import FoodItem

load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="RecipeAWaste API",
    description="Food waste reduction through recipe generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase & Groq
db = FirebaseDB()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class FoodItemInput(BaseModel):
    """Input model for adding food items via JSON."""
    name: str
    calorie: int
    protein: int
    expiry_date: Optional[str] = None  # ISO format string
    quantity: int = 1


class FoodItemOutput(BaseModel):
    """Output model for food items as JSON."""
    id: str
    name: str
    calorie: int
    protein: int
    expiry_date: Optional[str] = None
    quantity: int


class RecipeRequest(BaseModel):
    cuisine_type: Optional[str] = None




def fooditem_to_json(item: FoodItem, item_id: str = None) -> dict:
    """Convert FoodItem dataclass to JSON dict."""
    return {
        "id": getattr(item, '_id', item_id or 'unknown'),
        "name": item.name,
        "calorie": item.calorie,
        "protein": item.protein,
        "expiry_date": item.expiry_date.isoformat() if item.expiry_date else None,
        "quantity": FoodItem.get_quantity()
    }


def json_to_fooditem(data: FoodItemInput) -> FoodItem:
    """Convert JSON input to FoodItem dataclass."""
    expiry = datetime.fromisoformat(data.expiry_date) if data.expiry_date else None

    item = FoodItem(
        name=data.name,
        calorie=data.calorie,
        protein=data.protein,
        expiry_date=expiry
    )

    # Set quantity
    for _ in range(data.quantity - 1):
        item.increase_quantity()

    return item




@app.get("/")
async def root():
    """Health check."""
    return {
        "message": "RecipeAWaste API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/fooditems", response_model=List[FoodItemOutput])
async def get_all_items():
    """Get all food items from Firebase."""
    try:
        items = db.get_all_food_items()
        return [fooditem_to_json(item, getattr(item, '_id', None)) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fooditems/{item_id}", response_model=FoodItemOutput)
async def get_item(item_id: str):
    """Get a specific food item."""
    item = db.get_food_item(item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return fooditem_to_json(item, item_id)


@app.post("/api/fooditems", response_model=FoodItemOutput, status_code=201)
async def add_item(data: FoodItemInput):
    """Add a new food item."""
    try:
        item = json_to_fooditem(data)
        item_id = db.add_food_item(item)

        return fooditem_to_json(item, item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/fooditems/{item_id}")
async def delete_item(item_id: str):
    """Delete a food item."""
    success = db.delete_food_item(item_id)

    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted", "id": item_id}


@app.post("/api/fooditems/{item_id}/increase")
async def increase_qty(item_id: str):
    """Increase quantity."""
    success = db.increase_quantity(item_id)

    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

    item = db.get_food_item(item_id)
    return fooditem_to_json(item, item_id)


@app.post("/api/fooditems/{item_id}/decrease")
async def decrease_qty(item_id: str):
    """Decrease quantity."""
    success = db.decrease_quantity(item_id)

    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

    item = db.get_food_item(item_id)
    return fooditem_to_json(item, item_id)


@app.delete("/api/fooditems")
async def clear_all():
    """Delete all items."""
    count = db.delete_all_items()
    return {"message": "All items deleted", "count": count}


@app.post("/api/recipes/generate")
async def generate_recipe(request: RecipeRequest):
    """Generate recipe using Groq API."""
    try:
        # Load fridge from Firebase
        fridge = db.load_fridge()

        if fridge.is_empty():
            raise HTTPException(status_code=400, detail="Fridge is empty")

        # Get items sorted by expiry
        items = fridge.get_sorted_by_expiry()

        # Build ingredient list
        ingredients = "\n".join([
            f"- {item.name}: quantity {FoodItem.get_quantity()}, "
            f"{item.calorie} cal, {item.protein}g protein, "
            f"expires: {item.expiry_date.strftime('%Y-%m-%d') if item.expiry_date else 'N/A'}"
            for item in items
        ])

        # Groq prompt
        prompt = f"""From these ingredients in my fridge, create a recipe:

{ingredients}

{f"Cuisine type: {request.cuisine_type}" if request.cuisine_type else ""}

Prioritize ingredients expiring soonest. Include:
1. Recipe name
2. Ingredients with amounts
3. Step-by-step instructions
4. Prep/cook time
5. Nutrition per serving"""

        # Call Groq
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        recipe = completion.choices[0].message.content

        return {
            "recipe": recipe,
            "ingredients_used": [item.name for item in items[:5]]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fridge/summary")
async def fridge_summary():
    """Get fridge summary statistics."""
    try:
        fridge = db.load_fridge()

        return {
            "total_items": fridge.count(),
            "is_empty": fridge.is_empty(),
            "expiring_soon": len(fridge.get_expiring_soon(3))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/fridge/expiring-soon")
async def expiring_soon(days: int = 3):
    """Get items expiring soon."""
    try:
        fridge = db.load_fridge()
        items = fridge.get_expiring_soon(days)

        return [fooditem_to_json(item, getattr(item, '_id', None)) for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)