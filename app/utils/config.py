from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url:str
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    redis_host: str
    redis_port: str

    
    model_config =SettingsConfigDict(env_file=".env")


settings = Settings()
