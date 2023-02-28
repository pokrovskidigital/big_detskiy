from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='MONGODB_URL')
    db_name: str = Field(..., env='MONGODB_DATABASE')
    jwt_secret_key: str = "9f63d3214da92c45a40d3866a5fb93e998afca753a557fee0de7ba8d6551767c"
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 1000


settings = Settings()
