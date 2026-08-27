from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.db.repositories.product_repository_impl import SQLAlchemyProductRepository
from app.use_cases.product_use_cases import (
    CreateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase
)

from app.domain.repositories.category_repository import CategoryRepository
from app.infrastructure.db.repositories.category_repository_impl import SQLAlchemyCategoryRepository
from app.use_cases.category_use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)

# Product Dependencies
def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return SQLAlchemyProductRepository(session=db)

def get_create_product_use_case(
    repo: ProductRepository = Depends(get_product_repository)
) -> CreateProductUseCase:
    return CreateProductUseCase(repository=repo)

def get_get_product_use_case(
    repo: ProductRepository = Depends(get_product_repository)
) -> GetProductUseCase:
    return GetProductUseCase(repository=repo)

def get_list_products_use_case(
    repo: ProductRepository = Depends(get_product_repository)
) -> ListProductsUseCase:
    return ListProductsUseCase(repository=repo)

def get_update_product_use_case(
    repo: ProductRepository = Depends(get_product_repository)
) -> UpdateProductUseCase:
    return UpdateProductUseCase(repository=repo)

def get_delete_product_use_case(
    repo: ProductRepository = Depends(get_product_repository)
) -> DeleteProductUseCase:
    return DeleteProductUseCase(repository=repo)

# Category Dependencies
def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return SQLAlchemyCategoryRepository(session=db)

def get_create_category_use_case(
    repo: CategoryRepository = Depends(get_category_repository)
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(repository=repo)

def get_get_category_use_case(
    repo: CategoryRepository = Depends(get_category_repository)
) -> GetCategoryUseCase:
    return GetCategoryUseCase(repository=repo)

def get_list_categories_use_case(
    repo: CategoryRepository = Depends(get_category_repository)
) -> ListCategoriesUseCase:
    return ListCategoriesUseCase(repository=repo)

def get_update_category_use_case(
    repo: CategoryRepository = Depends(get_category_repository)
) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(repository=repo)

def get_delete_category_use_case(
    repo: CategoryRepository = Depends(get_category_repository)
) -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase(repository=repo)
