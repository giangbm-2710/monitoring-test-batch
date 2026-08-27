from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Category:
    id: Optional[int]
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate(self) -> None:
        """Domain validation logic."""
        if not self.name or not self.name.strip():
            raise ValueError("Category name cannot be empty")
