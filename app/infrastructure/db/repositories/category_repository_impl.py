from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.db.models.category_model import CategoryModel

class SQLAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            description=entity.description
        )

    async def create(self, category: Category) -> Category:
        db_model = self._to_model(category)
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return self._to_entity(db_model)

    async def get_by_id(self, category_id: int) -> Optional[Category]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.name == name)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.session.execute(
            select(CategoryModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(CategoryModel.id)))
        return result.scalar_one()

    async def update(self, category: Category) -> Category:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category.id)
        )
        db_model = result.scalar_one_or_none()
        if not db_model:
            raise ValueError(f"Category with id {category.id} not found")

        db_model.name = category.name
        db_model.description = category.description

        await self.session.commit()
        await self.session.refresh(db_model)
        return self._to_entity(db_model)

    async def delete(self, category_id: int) -> bool:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        db_model = result.scalar_one_or_none()
        if db_model:
            await self.session.delete(db_model)
            await self.session.commit()
            return True
        return False
