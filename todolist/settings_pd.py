import os

from pydantic import BaseSettings


class Settings_TDL(BaseSettings):
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD : str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST : str = os.getenv("DB_HOST")
    DB_PORT : str = os.getenv("DB_PORT")
    DJ_DEBUG : bool = os.getenv("DJ_DEBUG")
    DJANGO_ALLOWED_HOSTS: str = os.getenv("DJANGO_ALLOWED_HOSTS")
    DJ_SECRET_KEY : str = os.getenv("DJ_SECRET_KEY")
    SOCIAL_AUTH_VK_OAUTH2_KEY: str = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY")
    SOCIAL_AUTH_VK_OAUTH2_SECRET:str = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET")

    class Config:
          env_file = '../.env_local'
