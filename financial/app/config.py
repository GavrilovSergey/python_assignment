from pydantic import BaseSettings

class Settings(BaseSettings):
    sqlalchemy_database_url: str
    alphavantage_api_key: str

    class Config:
        env_file = 'app/.env'
        env_file_encoding = 'utf-8'