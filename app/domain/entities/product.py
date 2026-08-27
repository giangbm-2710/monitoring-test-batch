from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate(self) -> None:
        """Domain validation logic."""
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.price < 0:
            raise ValueError("Product price cannot be negative")
        if self.stock < 0:
            raise ValueError("Product stock cannot be negative")
