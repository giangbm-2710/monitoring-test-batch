from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
    CategoryAlreadyExistsException
)
from app.presentation.api.v1.dependencies import (
    get_create_category_use_case,
    get_get_category_use_case,
    get_list_categories_use_case,
    get_update_category_use_case,
    get_delete_category_use_case
)
from app.presentation.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse
)
from app.use_cases.category_use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate,
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case)
):
    try:
        category = await use_case.execute(
            name=payload.name,
            description=payload.description
        )
        return category
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    use_case: GetCategoryUseCase = Depends(get_get_category_use_case)
):
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/", response_model=CategoryListResponse)
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    use_case: ListCategoriesUseCase = Depends(get_list_categories_use_case)
):
    items, total = await use_case.execute(skip=skip, limit=limit)
    return CategoryListResponse(total=total, items=items)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    use_case: UpdateCategoryUseCase = Depends(get_update_category_use_case)
):
    try:
        return await use_case.execute(
            category_id=category_id,
            name=payload.name,
            description=payload.description
        )
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    use_case: DeleteCategoryUseCase = Depends(get_delete_category_use_case)
):
    try:
        await use_case.execute(category_id=category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
