from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.presentation.schemas.category_schema import CategoryResponse

class ProductBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Laptop Dell XPS 15"}, min_length=1, max_length=255)
    description: Optional[str] = Field(None, json_schema_extra={"example": "High performance laptop"})
    price: float = Field(..., json_schema_extra={"example": 1299.99}, ge=0.0)
    stock: int = Field(..., json_schema_extra={"example": 50}, ge=0)
    category_id: Optional[int] = Field(None, json_schema_extra={"example": 1})

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "Laptop Dell XPS 15"}, min_length=1, max_length=255)
    description: Optional[str] = Field(None, json_schema_extra={"example": "Updated description"})
    price: Optional[float] = Field(None, json_schema_extra={"example": 1199.99}, ge=0.0)
    stock: Optional[int] = Field(None, json_schema_extra={"example": 45}, ge=0)
    category_id: Optional[int] = Field(None, json_schema_extra={"example": 1})

class ProductResponse(ProductBase):
    id: int
    category: Optional[CategoryResponse] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    total: int
    items: List[ProductResponse]
