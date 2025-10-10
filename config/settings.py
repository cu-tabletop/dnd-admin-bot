from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import logging

class Settings(BaseSettings):
    # Обязательные поля
    BOT_TOKEN: str = Field(..., min_length=1)
    API_BASE_URL: str = Field(..., min_length=1)
    
    USE_API_STUBS: bool = False
    STUB_DELAY: float = 0.5  # Задержка для имитации сетевого запроса
    
    # Опциональные поля с значениями по умолчанию
    LOG_LEVEL: str = Field(default="INFO")
    API_TIMEOUT: int = Field(default=30)
    
    # Конфигурация модели - ИСПРАВЛЕННАЯ ВЕРСИЯ
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def setup_logging(level: str = "INFO"):
    """Настройка логирования с проверкой уровня"""
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level not in valid_levels:
        level = "INFO"
        
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("bot.log", encoding="utf-8")
        ]
    )

# Создаем экземпляр настроек
try:
    settings = Settings() # type: ignore
except Exception as e:
    logging.error(f"Ошибка загрузки настроек: {e}")
    raise

# Настраиваем логирование
setup_logging(settings.LOG_LEVEL)