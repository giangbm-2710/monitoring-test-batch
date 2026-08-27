from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.presentation.schemas.user_schema import UserResponse
from app.use_cases.user_use_cases import ListUsersUseCase, GetUserUseCase
from app.domain.exceptions.user_exceptions import UserNotFoundException
from app.presentation.api.v1.dependencies import (
    get_list_users_use_case,
    get_get_user_use_case
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    use_case: ListUsersUseCase = Depends(get_list_users_use_case)
):
    """Retrieve list of users with pagination."""
    users = await use_case.execute(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends(get_get_user_use_case)
):
    """Get a specific user by ID."""
    try:
        user = await use_case.execute(user_id)
        return user
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
