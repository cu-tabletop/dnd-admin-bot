import functools
from typing import Callable, Any
from models.models import InventoryItem, InventoryItemCreate, InventoryItemUpdate
from utils.logger import get_logger


def log_inventory_operation(operation: str):
    """Декоратор для логирования операций с инвентарем"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            try:
                character_id = kwargs.get("character_id")
                item_data = kwargs.get("item_data") or kwargs.get("item")

                logger.info(
                    f"Inventory {operation}: character_id={character_id}, "
                    f"item={getattr(item_data, 'name', 'Unknown')}"
                )
                result = await func(*args, **kwargs)
                logger.info(f"Inventory {operation} successful")
                return result
            except Exception as e:
                logger.error(f"Inventory {operation} failed: {e}")
                raise

        return wrapper

    return decorator


# Применяем декораторы к методам API клиента
class RealAPIClient:
    @log_inventory_operation("add")
    async def add_inventory_item(
        self, character_id: int, item: InventoryItemCreate
    ) -> InventoryItem:
        # существующая реализация
        pass

    @log_inventory_operation("update")
    async def update_inventory_item(
        self, item_id: int, item_data: InventoryItemUpdate
    ) -> InventoryItem:
        # существующая реализация
        pass

    @log_inventory_operation("delete")
    async def delete_inventory_item(self, item_id: int) -> bool:
        # существующая реализация
        pass
