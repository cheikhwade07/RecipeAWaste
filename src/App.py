from datetime import date

class FoodItem:
    quantity = 0
    def __init__(self, name: str, calorie: int, protein: int, expiry_date: date):
        self.name = name
        self.calorie = calorie
        self.protein = protein
        self.expiry_date = expiry_date
        FoodItem.quantity = 0

    def increase_quantity(self):
        FoodItem.quantity += 1

    def decrease_quantity(self):
        FoodItem.quantity -= 1


class Fridge:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
