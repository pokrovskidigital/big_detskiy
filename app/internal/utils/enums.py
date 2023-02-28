from enum import Enum


class ImageSizeEnum(str, Enum):
    SMALL = 'Small'
    MEDIUM = 'Medium'
    LARGE = "Large"


class SexEnum(str, Enum):
    MAN = 'Man'
    WOMAN = 'Woman'
    CHILD = 'Child'
    GIRL = 'Girl'
    BOY = 'Boy'
    UNISEX = 'Unisex'


class FieldTypeEnum(str):
    FLOAT = 'Float'
    INT = 'Int'
    BOOL = 'Bool'
    STRING = 'String'
