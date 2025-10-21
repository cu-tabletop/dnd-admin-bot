import pytest
from unittest.mock import AsyncMock, patch
from services.api_client import RealAPIClient, StubAPIClient
from models.models import InventoryItem, InventoryItemCreate, InventoryItemUpdate
from dialogs.inventory_management import on_item_name_input, on_edit_item_quantity


class TestInventoryFunctionality:
    @pytest.mark.asyncio
    async def test_add_inventory_item_flow(self):
        """Тест процесса добавления предмета"""
        mock_manager = AsyncMock()
        mock_manager.dialog_data = {"character_id": 1}
        mock_message = AsyncMock()

        # Тест ввода названия
        await on_item_name_input(mock_message, None, mock_manager, "Меч-кладенец")
        assert mock_manager.dialog_data["new_item_name"] == "Меч-кладенец"
        mock_message.answer.assert_called()

    @pytest.mark.asyncio
    async def test_edit_item_quantity_success(self):
        """Тест успешного изменения количества"""
        mock_manager = AsyncMock()
        mock_manager.dialog_data = {"selected_item_id": 1}
        mock_message = AsyncMock()

        with patch("services.api_client.create_api_client") as mock_api:
            mock_client = AsyncMock()
            mock_client.update_inventory_item.return_value = InventoryItem(
                id=1, name="Меч", description="Острый", quantity=5
            )
            mock_api.return_value = mock_client

            await on_edit_item_quantity(mock_message, None, mock_manager, "5")

            mock_client.update_inventory_item.assert_called_once()
            mock_message.answer.assert_called_with("✅ Количество изменено на: 5")
            mock_manager.switch_to.assert_called_once()

    @pytest.mark.asyncio
    async def test_edit_item_quantity_validation(self):
        """Тест валидации ввода количества"""
        mock_manager = AsyncMock()
        mock_manager.dialog_data = {"selected_item_id": 1}
        mock_message = AsyncMock()

        # Тест отрицательного значения
        await on_edit_item_quantity(mock_message, None, mock_manager, "-1")
        mock_message.answer.assert_called_with(
            "❌ Количество должно быть положительным числом"
        )

        # Тест нечислового ввода
        await on_edit_item_quantity(mock_message, None, mock_manager, "не число")
        mock_message.answer.assert_called_with("❌ Пожалуйста, введите целое число")


class TestStubInventory:
    @pytest.mark.asyncio
    async def test_stub_inventory_operations(self):
        """Тест операций с инвентарем в заглушках"""
        stub_client = StubAPIClient()

        # Добавление предмета
        new_item = InventoryItemCreate(
            name="Тестовый предмет",
            description="Описание тестового предмета",
            quantity=3,
        )

        added_item = await stub_client.add_inventory_item(1, new_item)
        assert added_item.name == "Тестовый предмет"
        assert added_item.quantity == 3

        # Получение инвентаря
        inventory = await stub_client.get_character_inventory(1)
        assert any(item.name == "Тестовый предмет" for item in inventory)

        # Обновление предмета
        update_data = InventoryItemUpdate(quantity=10)
        updated_item = await stub_client.update_inventory_item(
            added_item.id, update_data
        )
        assert updated_item.quantity == 10

        # Удаление предмета
        result = await stub_client.delete_inventory_item(added_item.id)
        assert result is True

    @pytest.mark.asyncio
    async def test_stub_inventory_persistence(self):
        """Тест сохранения данных в заглушках"""
        stub_client = StubAPIClient()

        # Добавляем предмет
        new_item = InventoryItemCreate(name="Персистентный предмет", quantity=1)
        added_item = await stub_client.add_inventory_item(1, new_item)

        # Проверяем что предмет сохранился
        inventory = await stub_client.get_character_inventory(1)
        assert any(item.id == added_item.id for item in inventory)
