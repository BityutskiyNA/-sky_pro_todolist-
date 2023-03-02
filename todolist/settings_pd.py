import os

from pydantic import BaseSettings


class Settings_TDL(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    DB_HOST : str = os.getenv("DB_HOST")
    DB_PORT : str = os.getenv("DB_PORT")
    DJ_DEBUG : bool = os.getenv("DJ_DEBUG")
    DJANGO_ALLOWED_HOSTS : str = os.getenv("DJANGO_ALLOWED_HOSTS")
    SOCIAL_AUTH_VK_OAUTH2_KEY: str = os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY")
    SOCIAL_AUTH_VK_OAUTH2_SECRET:str = os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET")

    # class Config:
    #     validate_all = False
    #     validate_assignment = False
    # #      env_file = '../.env_local'
