from typing import List, Tuple, Optional
from app.domain.entities.category import Category
from app.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
    CategoryAlreadyExistsException
)
from app.domain.repositories.category_repository import CategoryRepository

class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, name: str, description: Optional[str] = None) -> Category:
        existing = await self.repository.get_by_name(name)
        if existing:
            raise CategoryAlreadyExistsException(name)

        category = Category(id=None, name=name, description=description)
        category.validate()
        return await self.repository.create(category)

class GetCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: int) -> Category:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundException(category_id)
        return category

class ListCategoriesUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 100) -> Tuple[List[Category], int]:
        categories = await self.repository.list(skip=skip, limit=limit)
        total = await self.repository.count()
        return categories, total

class UpdateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Category:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundException(category_id)

        if name is not None and name != category.name:
            existing = await self.repository.get_by_name(name)
            if existing:
                raise CategoryAlreadyExistsException(name)
            category.name = name

        if description is not None:
            category.description = description

        category.validate()
        return await self.repository.update(category)

class DeleteCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: int) -> None:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundException(category_id)
        await self.repository.delete(category_id)
