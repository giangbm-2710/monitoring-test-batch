from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user_model import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            full_name=model.full_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalars().first()
        return self._to_entity(model) if model else None

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.session.execute(select(UserModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    async def create(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)
