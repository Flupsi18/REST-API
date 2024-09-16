from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://mongos:27017/vda?retryWrites=true&w=majority"
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = "testkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 60 Minuten
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 Tage
    DOCS_URL: str = "/api/docs"
    PROJECT_NAME: str = "REST-API-template"
    PROJECT_DESCRIPTION: str = "Template for REST-API"


settings = Settings()
