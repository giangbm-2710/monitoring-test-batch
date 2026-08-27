from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.entities.product import Product

class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        """Create a new product."""
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Find a product by ID."""
        pass

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 10, category_id: Optional[int] = None) -> Tuple[List[Product], int]:
        """List products with pagination and filtering."""
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        """Update an existing product."""
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        """Delete a product by ID."""
        pass
