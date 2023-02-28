from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(max_length=200)
    parent: Optional[str]
