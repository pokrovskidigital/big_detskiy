from typing import List

import requests
from beanie import WriteRules
from fastapi import APIRouter

from app.internal.models.catalog import Product, Image
from app.internal.models.user import User, UserFactory
from app.internal.utils.models import CommonResponse, Content
from app.internal.utils.services import generate_fake_images

router = APIRouter(
    prefix='/api/v1/utils'
)


@router.get('/generate_fake/')
async def generate_fake():
    images: List[Image] = await generate_fake_images()
    print(images)
    content = Content(message='ok').json()
    return CommonResponse(status_code=200, content=content)
