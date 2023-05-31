from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/postgres"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "qwerty"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.test.com"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = "cloudinary name"
    cloudinary_api_key: int = "0000000000000000"
    cloudinary_api_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
