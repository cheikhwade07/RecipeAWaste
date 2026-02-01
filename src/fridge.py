
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, date, timedelta
from food_item import FoodItem


@dataclass
class Fridge:

    def __init__(self):

        self._items: Dict[str, FoodItem] = {}

    def add_item(self, item: FoodItem) -> bool:

        item_key = item.name.lower()

        if item_key in self._items:
            # Item already exists, add to its weight
            self._items[item_key].weight += item.weight
            print(f"Increased weight of '{item.name}' to {self._items[item_key].weight}kg")
            return False
        else:
            # New item, add to fridge
            self._items[item_key] = item
            print(f"Added new item: '{item.name}'")
            return True

    def remove_item(self, name: str) -> Optional[FoodItem]:

        item_key = name.lower()

        if item_key in self._items:
            removed_item = self._items.pop(item_key)
            print(f"Removed '{removed_item.name}' from fridge")
            return removed_item
        else:
            print(f"Item '{name}' not found in fridge")
            return None

    def get_item(self, name: str) -> Optional[FoodItem]:

        return self._items.get(name.lower())

    def get_all_items(self) -> List[FoodItem]:

        return list(self._items.values())

    def get_items_dict(self) -> Dict[str, FoodItem]:

        return self._items.copy()

    def is_empty(self) -> bool:

        return len(self._items) == 0

    def count(self) -> int:

        return len(self._items)

    def clear(self) -> None:
        self._items.clear()
        print("Fridge cleared")



    def get_expiring_soon(self, days: int = 3) -> List[FoodItem]:

        threshold_date = datetime.now() + timedelta(days=days)

        expiring_items = [
            item for item in self._items.values()
            if item.expiry_date and item.expiry_date <= threshold_date
        ]

        # Sort by expiry date (soonest first)
        expiring_items.sort(key=lambda x: x.expiry_date or datetime.max)

        return expiring_items

    def get_expired_items(self) -> List[FoodItem]:

        now = datetime.now()

        expired = [
            item for item in self._items.values()
            if item.expiry_date and item.expiry_date < now
        ]

        return expired

    def get_items_by_category(self, category: str) -> List[FoodItem]:

        category_lower = category.lower()

        return [
            item for item in self._items.values()
            if category_lower in item.name.lower()
        ]

    def search_items(self, query: str) -> List[FoodItem]:

        query_lower = query.lower()

        return [
            item for item in self._items.values()
            if query_lower in item.name.lower()
        ]


    def get_sorted_by_expiry(self) -> List[FoodItem]:

        items_with_expiry = [
            item for item in self._items.values()
            if item.expiry_date
        ]

        items_with_expiry.sort(key=lambda x: x.expiry_date)

        # Add items without expiry date at the end
        items_without_expiry = [
            item for item in self._items.values()
            if not item.expiry_date
        ]

        return items_with_expiry + items_without_expiry

    def get_sorted_by_weight(self, descending: bool = False) -> List[FoodItem]:
        items = self.get_all_items()
        items.sort(key=lambda x: x.weight, reverse=descending)
        return items



    def display_all(self) -> None:

        if self.is_empty():
            print("Fridge is empty!")
            return

        print(f"\n{'=' * 60}")
        print(f"FRIDGE CONTENTS ({self.count()} items)")
        print(f"{'=' * 60}")

        for item in self.get_sorted_by_expiry():
            expiry_str = item.expiry_date.strftime("%Y-%m-%d") if item.expiry_date else "No expiry"
            print(f"• {item.name:20} | Weight: {item.weight}kg | Expires: {expiry_str}")

        print(f"{'=' * 60}\n")

    def display_expiring_soon(self, days: int = 3) -> None:

        expiring = self.get_expiring_soon(days)

        if not expiring:
            print(f"No items expiring in the next {days} days!")
            return

        print(f"\nITEMS EXPIRING IN {days} DAYS:")
        for item in expiring:
            days_left = (item.expiry_date - datetime.now()).days
            print(f"  • {item.name} - {days_left} days left ({item.expiry_date.strftime('%Y-%m-%d')})")
        print()


    def __str__(self) -> str:

        return f"Fridge({self.count()} items)"

    def __repr__(self) -> str:

        return f"Fridge(items={list(self._items.keys())})"