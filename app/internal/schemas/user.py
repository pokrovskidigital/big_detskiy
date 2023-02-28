from bson import ObjectId
from pydantic import BaseModel, Field


class SendOTP(BaseModel):
    # _id: ObjectId
    phone_number: str = Field(..., max_length=11, min_length=11)


class VerifyOTP(BaseModel):
    # _id: ObjectId
    phone_number: str = Field(..., max_length=11, min_length=11)
    code: int = Field(default=0)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone_number: str | None = None
