import pytest
from unittest.mock import AsyncMock, patch
from services.api_client import APIClient, StubAPIClient
from models.models import Character
from dialogs.character_management import on_rating_input, on_quick_rating_change

class TestRatingFunctionality:
    @pytest.mark.asyncio
    async def test_rating_input_success(self):
        """Тест успешного ввода рейтинга"""
        mock_manager = AsyncMock()
        mock_manager.dialog_data = {"character_id": 1}
        mock_message = AsyncMock()
        
        with patch('services.api_client.get_api_client') as mock_api:
            mock_client = AsyncMock()
            mock_client.update_character_rating.return_value = Character(id=1, name="Test", level=5, rating=95, company_id=1)
            mock_api.return_value = mock_client
            
            await on_rating_input(mock_message, None, mock_manager, "95")
            
            mock_client.update_character_rating.assert_called_once_with(1, 95)
            mock_message.answer.assert_called_with("✅ Рейтинг успешно изменен на 95")
            mock_manager.back.assert_called_once()

    @pytest.mark.asyncio
    async def test_rating_input_validation(self):
        """Тест валидации ввода рейтинга"""
        mock_manager = AsyncMock()
        mock_manager.dialog_data = {"character_id": 1}
        mock_message = AsyncMock()
        
        # Тест отрицательного значения
        await on_rating_input(mock_message, None, mock_manager, "-10")
        mock_message.answer.assert_called_with("❌ Рейтинг не может быть отрицательным")
        
        # Тест слишком большого значения
        await on_rating_input(mock_message, None, mock_manager, "1500")
        mock_message.answer.assert_called_with("❌ Рейтинг не может превышать 1000")
        
        # Тест нечислового ввода
        await on_rating_input(mock_message, None, mock_manager, "не число")
        mock_message.answer.assert_called_with("❌ Пожалуйста, введите целое число")

    @pytest.mark.asyncio 
    async def test_quick_rating_change(self):
        """Тест быстрого изменения рейтинга"""
        mock_manager = AsyncMock()
        mock_manager.dialog_data = {"character_id": 1}
        mock_callback = AsyncMock()
        
        with patch('services.api_client.create_api_client') as mock_api:
            mock_client = AsyncMock()
            mock_client.get_character.return_value = Character(id=1, name="Test", level=5, rating=50, company_id=1)
            mock_client.update_character_rating.return_value = Character(id=1, name="Test", level=5, rating=55, company_id=1)
            mock_api.return_value = mock_client
            
            await on_quick_rating_change(mock_callback, None, mock_manager, "5")
            
            mock_client.get_character.assert_called_with(1)
            mock_client.update_character_rating.assert_called_with(1, 55)
            mock_manager.show.assert_called_once()

class TestStubAPIRating:
    @pytest.mark.asyncio
    async def test_stub_rating_update(self):
        """Тест обновления рейтинга в заглушках"""
        stub_client = StubAPIClient()
        
        # Получаем начальное состояние
        character = await stub_client.get_character(1)
        initial_rating = character.rating
        
        # Обновляем рейтинг
        updated_character = await stub_client.update_character_rating(1, initial_rating + 10)
        
        # Проверяем
        assert updated_character.rating == initial_rating + 10
        
        # Проверяем что изменения сохранились
        character_after = await stub_client.get_character(1)
        assert character_after.rating == initial_rating + 10