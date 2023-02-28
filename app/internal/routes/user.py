import requests
from beanie import WriteRules
from fastapi import APIRouter

from app.internal.models.catalog import Product, Image
from app.internal.models.user import User, UserFactory
from app.internal.utils.models import CommonResponse, Content

router = APIRouter(
    prefix='/api/v1/users'
)


@router.post("/create/")
async def create_user(user: User) -> CommonResponse:
    await User.save(user)
    content = Content(message='ok').json()
    return CommonResponse(status_code=200, content=content)


