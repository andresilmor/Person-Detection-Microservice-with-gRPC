from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    development: bool

    class Config:
        env_file = ".env"
