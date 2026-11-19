import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str

    # Указываем Pydantic, что нужно читать данные из файла ".env"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


    # Наше свойство, которое само соберёт красивую длинную строку для SQLAlchemy
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

# Создаём объект, который будем импортировать в другие файлы
# создать экземпляр класса
settings = Settings()