from fastapi import APIRouter, Query

from app.internal.models.catalog import Product, Image, Category
from app.internal.utils.models import Content, CommonResponse, CommonHTTPException

router = APIRouter(
    prefix='/api/v1/catalog'
)


@router.get('/all_products')
async def all_products(page: int = Query(default=1, gte=1, description='Page param'),
                       page_size: int = Query(default=40, gt=0, lt=500)) -> CommonResponse:
    products = await Product.find_all().limit(page_size).skip(page_size * (page - 1)).to_list()
    # print(products)
    content = Content(message='ok', result=products).json()
    return CommonResponse(content=content)


@router.post('/create_category/')
async def create_category(category: Category) -> CommonResponse:
    await Category.save(category)
    content = Content(message='ok').json()
    return CommonResponse(status_code=200, content=content)
