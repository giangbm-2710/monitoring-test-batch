from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class CategoryBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Electronics"}, min_length=1, max_length=100)
    description: Optional[str] = Field(None, json_schema_extra={"example": "Electronic devices and gadgets"})

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "Consumer Electronics"}, min_length=1, max_length=100)
    description: Optional[str] = Field(None, json_schema_extra={"example": "Updated description"})

class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CategoryListResponse(BaseModel):
    total: int
    items: List[CategoryResponse]
