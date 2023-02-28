from datetime import datetime, date
from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import Field, BaseModel
from .catalog import Product
from pydantic_factories import ModelFactory

from ..utils.enums import SexEnum


# from odmantic import Model, Field, Reference, EmbeddedModel

class Child(BaseModel):
    name: str = Field()
    birthday: date = Field()
    sex: SexEnum = SexEnum.UNISEX


class PhoneCode(Document):
    # _id: PydanticObjectId
    code: int
    is_verified: bool = False


class User(Document):
    # username: str
    name: str = Field()
    surname: str = Field()
    birthday: date = Field()
    children: Optional[List[Child]]
    phone_number: str = Field(max_length=11, min_length=11)
    phone_code: Optional[Link[PhoneCode]]
    is_active: bool = False
    favorite_products: Optional[List[Link[Product]]]
    watched_products: Optional[List[Link[Product]]]
    recommendation_products: Optional[List[Link[Product]]]


class UserFactory(ModelFactory[User]):
    __model__ = User
