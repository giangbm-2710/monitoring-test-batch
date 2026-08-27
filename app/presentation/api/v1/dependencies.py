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
