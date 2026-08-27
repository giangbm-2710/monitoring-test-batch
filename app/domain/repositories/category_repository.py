from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.category import Category

class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Category]:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[Category]:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, category_id: int) -> bool:
        pass
