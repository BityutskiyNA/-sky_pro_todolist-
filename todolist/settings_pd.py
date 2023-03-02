from pydantic import BaseSettings


class Settings_TDL(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    DB_HOST : str
    DB_PORT : str
    DJ_DEBUG : bool
    DJANGO_ALLOWED_HOSTS : str
    SOCIAL_AUTH_VK_OAUTH2_KEY: str
    SOCIAL_AUTH_VK_OAUTH2_SECRET:str

    # class Config:
    #     validate_all = False
    #     validate_assignment = False
    # #      env_file = '../.env_local'
