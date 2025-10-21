# from config.settings import settings
# from services.api_client import create_api_client
# from utils.logger import get_logger

# logger = get_logger(__name__)

# def toggle_stub_mode(enable: bool | None = None):
#     """Переключение режима заглушек"""
#     if enable is None:
#         enable = not settings.USE_API_STUBS

#     settings.USE_API_STUBS = enable
#     mode = "ВКЛЮЧЕН" if enable else "ВЫКЛЮЧЕН"
#     logger.info(f"Режим заглушек API {mode}")

#     # Пересоздаем клиент API
#     from services.api_client import api_client
#     global api_client
#     api_client = create_api_client()

#     return enable

# def get_stub_status() -> dict:
#     """Получение статуса заглушек"""
#     return {
#         "use_stubs": settings.USE_API_STUBS,
#         "stub_delay": settings.STUB_DELAY,
#         "api_base_url": settings.API_BASE_URL
#     }
