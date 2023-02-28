from datetime import timedelta

from beanie import WriteRules
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.configuration.settings import settings
from app.internal.models.user import User, PhoneCode
from app.internal.schemas.user import SendOTP, VerifyOTP, Token
from app.internal.utils.user import generate_phone_code, authenticate_user, create_access_token
from app.internal.utils.models import Content, CommonResponse, CommonHTTPException

router = APIRouter(
    prefix='/api/v1/auth'
)


@router.post('/send_otp/')
async def send_otp(otp: SendOTP) -> CommonResponse:
    user = await User.find_one(User.phone_number == otp.phone_number)
    code = PhoneCode(code=generate_phone_code())
    if user:
        user.phone_code = code
        await User.save(user, link_rule=WriteRules.WRITE)
        # otp_code = OTP(code=user.phone_code.code)
        content = Content(message='Phone code sent', result=code)
        return CommonResponse(status_code=200, content=content.json())
    else:
        raise HTTPException(status_code=400, detail="Can't find phone user")


@router.post('/verify_otp/')
async def verify_otp(otp: VerifyOTP) -> CommonResponse:
    phone_code = await PhoneCode.find_one(PhoneCode.code == otp.code)
    if phone_code:
        phone_code.is_verified = True
        await PhoneCode.save(phone_code)
        content = Content(message='Phone code verified')
        return CommonResponse(status_code=200, content=content.json())
    else:
        raise HTTPException(status_code=400, detail='sad')


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: SendOTP):
    user = await authenticate_user(form_data.phone_number)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or phone_code",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.phone_number}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
