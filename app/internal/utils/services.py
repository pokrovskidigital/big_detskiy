import random
from typing import List

from beanie import WriteRules
from faker import Faker
from app.internal.models.catalog import Image, ImageUrl
from .enums import ImageSizeEnum

fake = Faker()
Faker.seed(1234)


async def gen_fake_url():
    return fake.url() + fake.file_path()[1:]


async def generate_fake_images(min_count: int = 2, max_count: int = 5) -> List[Image]:
    # fake_image_url = lambda faker_obj: faker_obj.url() + faker_obj.file_path()[1:]
    images: List[Image] | List = []
    for i in range(random.randint(min_count, max_count)):
        image_urls = []
        for size in list(ImageSizeEnum):
            image_urls.append(ImageUrl(size_type=size, url_webp=await gen_fake_url(), url_jpg=await gen_fake_url()))
        img = Image(title=fake.file_name(), urls=image_urls)
        image = await Image.save(img, link_rule=WriteRules.WRITE)
        images.append(image)

    return images


# async def generate_fake_category