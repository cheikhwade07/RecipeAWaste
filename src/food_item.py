from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar, Optional


@dataclass
class FoodItem:
    name: str
    weight: float
    expiry_date: Optional[datetime] = None


    # class variable shared by all instances
    quantity: ClassVar[int] = 0

    def __post_init__(self):
        # preserve original Java behaviour (resets class quantity on new instance)
        FoodItem.quantity = 0

    def increase_quantity(self) -> None:
        """Increase the shared `quantity` by 1."""
        FoodItem.quantity += 1

    def decrease_quantity(self) -> None:
        """Decrease the shared `quantity` by 1."""
        FoodItem.quantity -= 1

    @classmethod
    def get_quantity(cls) -> int:
        """Return the current shared quantity."""
        return cls.quantity
