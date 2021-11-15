# pydantic validate env variables from file
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_HOSTNAME: str
    DB_PORT: str
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "qwe777asd"
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
settings = Settings()