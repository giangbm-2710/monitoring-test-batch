from typing import List, Optional
from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.domain.exceptions.product_exceptions import ProductNotFoundException, InvalidProductDataException

class CreateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, name: str, price: float, stock: int, category: str, description: Optional[str] = None) -> Product:
        product = Product(
            id=None,
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )
        try:
            product.validate()
        except ValueError as e:
            raise InvalidProductDataException(str(e))

        return await self.repository.create(product)


class GetProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, product_id: int) -> Product:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        return product


class ListProductsUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 10, category: Optional[str] = None) -> List[Product]:
        return await self.repository.list_all(skip=skip, limit=limit, category=category)


class UpdateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(
        self,
        product_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
        category: Optional[str] = None
    ) -> Product:
        existing_product = await self.repository.get_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundException(product_id)

        updated_product = Product(
            id=existing_product.id,
            name=name if name is not None else existing_product.name,
            description=description if description is not None else existing_product.description,
            price=price if price is not None else existing_product.price,
            stock=stock if stock is not None else existing_product.stock,
            category=category if category is not None else existing_product.category,
            created_at=existing_product.created_at,
            updated_at=existing_product.updated_at
        )

        try:
            updated_product.validate()
        except ValueError as e:
            raise InvalidProductDataException(str(e))

        return await self.repository.update(updated_product)


class DeleteProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def execute(self, product_id: int) -> bool:
        existing_product = await self.repository.get_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundException(product_id)
        return await self.repository.delete(product_id)
