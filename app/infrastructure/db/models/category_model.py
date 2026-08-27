from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    products = relationship("ProductModel", back_populates="category_rel")
