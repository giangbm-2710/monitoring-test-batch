from typing import List, Optional, Tuple
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload
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
            category_id=model.category_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def create(self, product: Product) -> Product:
        db_model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category_id=product.category_id
        )
        self.session.add(db_model)
        await self.session.commit()
        return await self.get_by_id(db_model.id)

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        query = select(ProductModel).options(selectinload(ProductModel.category_rel)).where(ProductModel.id == product_id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()
        if db_model:
            entity = self._to_entity(db_model)
            # Attach category object for presentation layer if loaded
            if db_model.category_rel:
                setattr(entity, "category", db_model.category_rel)
            return entity
        return None

    async def list_all(self, skip: int = 0, limit: int = 10, category_id: Optional[int] = None) -> Tuple[List[Product], int]:
        query = select(ProductModel).options(selectinload(ProductModel.category_rel))
        count_query = select(func.count(ProductModel.id))

        if category_id:
            query = query.where(ProductModel.category_id == category_id)
            count_query = count_query.where(ProductModel.category_id == category_id)

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        db_models = result.scalars().all()

        total_res = await self.session.execute(count_query)
        total = total_res.scalar_one()

        entities = []
        for m in db_models:
            e = self._to_entity(m)
            if m.category_rel:
                setattr(e, "category", m.category_rel)
            entities.append(e)

        return entities, total

    async def update(self, product: Product) -> Product:
        query = select(ProductModel).where(ProductModel.id == product.id)
        result = await self.session.execute(query)
        db_model = result.scalar_one_or_none()

        if db_model:
            db_model.name = product.name
            db_model.description = product.description
            db_model.price = product.price
            db_model.stock = product.stock
            db_model.category_id = product.category_id

            await self.session.commit()
            return await self.get_by_id(db_model.id)
        raise ValueError(f"Product with id {product.id} does not exist in database")

    async def delete(self, product_id: int) -> bool:
        stmt = delete(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
