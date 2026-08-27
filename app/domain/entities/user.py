from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
