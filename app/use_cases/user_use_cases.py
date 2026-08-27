from typing import List, Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.exceptions.user_exceptions import UserNotFoundException

class ListUsersUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repository.list_users(skip=skip, limit=limit)

class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user
