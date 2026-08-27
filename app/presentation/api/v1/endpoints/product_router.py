from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.domain.exceptions.product_exceptions import ProductNotFoundException, InvalidProductDataException
from app.presentation.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)
from app.presentation.api.v1.dependencies import (
    get_create_product_use_case,
    get_get_product_use_case,
    get_list_products_use_case,
    get_update_product_use_case,
    get_delete_product_use_case
)
from app.use_cases.product_use_cases import (
    CreateProductUseCase,
    GetProductUseCase,
    ListProductsUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase
)

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case)
):
    """Create a new product."""
    try:
        product = await use_case.execute(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            stock=payload.stock,
            category=payload.category
        )
        return product
    except InvalidProductDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    use_case: GetProductUseCase = Depends(get_get_product_use_case)
):
    """Get a product by ID."""
    try:
        return await use_case.execute(product_id=product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=ProductListResponse)
async def list_products(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Items to limit"),
    category: Optional[str] = Query(None, description="Filter by category"),
    use_case: ListProductsUseCase = Depends(get_list_products_use_case)
):
    """List products with pagination and category filter."""
    products = await use_case.execute(skip=skip, limit=limit, category=category)
    return ProductListResponse(
        total=len(products),
        items=[ProductResponse.model_validate(p) for p in products]
    )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    use_case: UpdateProductUseCase = Depends(get_update_product_use_case)
):
    """Update a product by ID."""
    try:
        return await use_case.execute(
            product_id=product_id,
            name=payload.name,
            description=payload.description,
            price=payload.price,
            stock=payload.stock,
            category=payload.category
        )
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidProductDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    use_case: DeleteProductUseCase = Depends(get_delete_product_use_case)
):
    """Delete a product by ID."""
    try:
        await use_case.execute(product_id=product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
