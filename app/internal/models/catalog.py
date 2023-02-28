from datetime import datetime

from ..utils.enums import SexEnum, ImageSizeEnum, FieldTypeEnum
from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, Json
from pydantic import Field
from pydantic_factories import ModelFactory
from slugify import slugify

from ..utils.models import TreeModel


class ExtraField(BaseModel):
    field_name: str
    field_type: FieldTypeEnum = FieldTypeEnum.BOOL
    value: int | bool | str | float


class ImageUrl(BaseModel):
    size_type: ImageSizeEnum = ImageSizeEnum.MEDIUM
    url_webp: str = Field(...)
    url_jpg: str = Field(...)


class Dimensions(BaseModel):
    width: float = Field()
    height: float = Field()
    length: float = Field()
    weight: float = Field()


class Icon(BaseModel):
    icon_url: str = Field(...)


class Info(BaseModel):
    sex: SexEnum = SexEnum.MAN
    description: str = Field()
    seo_description: str = Field()
    seo_title: str = Field()
    seo_keys: str = Field()


class Price(BaseModel):
    price: float = 0
    old_price: float = 0


class Leftover(BaseModel):
    size: Link["Size"]
    count: int = 0
    price: Price


class Composition(BaseModel):
    materials: List[Link['Material']]


class Material(Document):
    title: str = Field(...)
    percent: int = Field(default=100)


class Age(Document):
    title: str = Field(..., max_length=200)


class Size(Document):
    title: str = Field(..., max_length=200)
    slug: str = Field(max_length=200)


class Image(Document):
    title: str
    urls: List['ImageUrl'] | None


class MainDocument(Document):
    title: str = Field(..., max_length=200)
    slug: str = Field(max_length=200)
    seo_data: Optional[List[Info]] = []

    def __init__(self, *args, **kwargs):
        super(MainDocument, self).__init__(*args, **kwargs)
        self.slug = slugify(self.title)

    class Settings:
        is_root = True


class Series(MainDocument):
    ...


class Character(MainDocument):
    ...


class ManufactureCountry(MainDocument):
    ...
    # def __init__(self):
    #     super(MainDocument, self).__init__()
    #     self.slug = slugify(self.title)


class Brand(MainDocument):
    icon: Icon


class Color(MainDocument):
    seo_data: None


class Category(TreeModel):
    title: str = Field(..., max_length=200)
    slug: str = Field(max_length=200)
    parent: Optional[Link['Category']]

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)


class Product(MainDocument):
    sku: str = Field(..., max_length=200)
    sex: SexEnum = SexEnum.MAN
    category: Link['Category']
    extra_categories: List[Link['Category']]
    colors: List[Link['Color']]
    characters: Optional[List[Link['Character']]]
    series: Optional[List[Link['Series']]]
    age: Optional[Link['Age']]
    manufacture_country: Optional[Link['ManufactureCountry']]
    dimensions: Dimensions
    seo_data: Info
    price: Price
    composition: Optional[Composition]
    images: Optional[List[Link['Image']]]
    brand: Link[Brand]
    leftovers: List[Leftover]
    extra_fields: Optional[List['ExtraField']]
    extra_content: Json | None
    date_of_creation: datetime | None
    date_of_publication: datetime | None
    show_in_news: bool = False
    participate_in_the_sale: bool = False


Product.update_forward_refs()
Image.update_forward_refs()
Category.update_forward_refs()
Composition.update_forward_refs()
Leftover.update_forward_refs()

# class ProductFactory(ModelFactory[Product]):
#     __model__ = Product
