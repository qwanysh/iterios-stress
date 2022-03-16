from pydantic import BaseSettings, constr, conint


class Settings(BaseSettings):
    iterios_api_key: constr(min_length=1)
    request_count: conint(gt=0)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
