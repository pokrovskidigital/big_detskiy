from datetime import datetime, timedelta
from random import randint

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.configuration.settings import settings
from beanie import DeleteRules
from jose import jwt, JWTError

from app.internal.models import User, PhoneCode
from app.internal.schemas.user import TokenData
from app.internal.utils.models import CommonHTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_phone_code():
    return randint(100000, 999999)


async def get_user(phone_number):
    user = await User.find_one(User.phone_number == phone_number)
    if user:
        await user.fetch_all_links()
        return user
    return None


async def authenticate_user(phone_number):
    user = await get_user(phone_number)

    if user.phone_code:
        if user.phone_code.code:
            code = await PhoneCode.find_one(PhoneCode.code == user.phone_code.code)
            user.phone_code = None
            await User.save(user)
            await PhoneCode.delete(code, link_rule=DeleteRules.DELETE_LINKS)

            return user
    return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = CommonHTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(phone_number=username)
    except JWTError:
        raise credentials_exception
    user = get_user(phone_number=token_data.phone_number)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
