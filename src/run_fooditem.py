"""Small runner demonstrating `FoodItem` usage in Python."""

from datetime import datetime

from food_item import FoodItem


def main() -> None:
    # Create a FoodItem instance (note: this resets class quantity to 0)
    item = FoodItem(name="Apple", calorie=95, protein=0, expiry_date=datetime(2026, 1, 31))
    print("Created:", item)
    print("Initial shared quantity:", FoodItem.get_quantity())

    item.increase_quantity()
    print("After increase:", FoodItem.get_quantity())

    item.decrease_quantity()
    print("After decrease:", FoodItem.get_quantity())


if __name__ == "__main__":
    main()
