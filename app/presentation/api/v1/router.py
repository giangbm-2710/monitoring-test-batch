from fastapi import APIRouter
from app.presentation.api.v1.endpoints.product_router import router as product_router
from app.presentation.api.v1.endpoints.category_router import router as category_router
from app.presentation.api.v1.endpoints.user_router import router as user_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(product_router)
api_router.include_router(category_router)
api_router.include_router(user_router)
