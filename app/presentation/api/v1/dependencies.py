from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.repositories.product_repository_impl import SQLAlchemyProductRepository
from app.infrastructure.db.repositories.user_repository_impl import SQLAlchemyUserRepository
from app.use_cases.product_use_cases import (
    CreateProductUseCase, GetProductUseCase, ListProductsUseCase, UpdateProductUseCase, DeleteProductUseCase
)
from app.use_cases.user_use_cases import ListUsersUseCase, GetUserUseCase

def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return SQLAlchemyProductRepository(session=db)

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session=db)

def get_list_users_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> ListUsersUseCase:
    return ListUsersUseCase(repository=repo)

def get_get_user_use_case(
    repo: UserRepository = Depends(get_user_repository)
) -> GetUserUseCase:
    return GetUserUseCase(repository=repo)

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

