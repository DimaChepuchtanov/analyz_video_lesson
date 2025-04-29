from pydantic import BaseSettings


class Setting(BaseSettings):
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    POSTGRES_DATABASE: str
    SECRET_KEY: str = 'UpywWKvxUSi8gpBUYS_ZUX0r_TpgY9ymjoEubeXxhU0='

    class Config:
        env = '.env'


setting = Setting()
