from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.models.product_model import ProductModel

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: ProductModel) -> Product:
        """Convert ORM model to Domain entity."""
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            stock=model.stock,
            category=model.category,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def create(self, product: Product) -> Product:
        db_model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=product.category
        )
        self.session.add(db_model)
        await self.session.flush()
        await self.session.refresh(db_model)
        return self._to_entity(db_model)

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()
        if db_model:
            return self._to_entity(db_model)
        return None

    async def list_all(self, skip: int = 0, limit: int = 10, category: Optional[str] = None) -> List[Product]:
        query = select(ProductModel)
        if category:
            query = query.where(ProductModel.category == category)
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        db_models = result.scalars().all()
        return [self._to_entity(m) for m in db_models]

    async def update(self, product: Product) -> Product:
        query = select(ProductModel).where(ProductModel.id == product.id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()
        
        if db_model:
            db_model.name = product.name
            db_model.description = product.description
            db_model.price = product.price
            db_model.stock = product.stock
            db_model.category = product.category
            
            await self.session.flush()
            await self.session.refresh(db_model)
            return self._to_entity(db_model)
        raise ValueError(f"Product with id {product.id} does not exist in database")

    async def delete(self, product_id: int) -> bool:
        stmt = delete(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
