import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.api_client import APIClient, get_api_client
from services.stub_api_client import StubAPIClient
from models.models import Company, Character, InventoryItem
from config.settings import settings

class TestRealAPIClient:
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.mark.asyncio
    async def test_get_companies_success(self, api_client):
        mock_data = [{"id": 1, "name": "Test Company"}]
        
        with patch('aiohttp.ClientSession.request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value.__aenter__.return_value.status = 200
            mock_request.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_data)
            
            companies = await api_client.get_companies()
            
            assert len(companies) == 1
            assert companies[0].id == 1
            assert companies[0].name == "Test Company"

class TestStubAPIClient:
    @pytest.fixture
    def stub_client(self):
        return StubAPIClient()
    
    @pytest.mark.asyncio
    async def test_get_companies(self, stub_client):
        companies = await stub_client.get_companies()
        assert len(companies) > 0
        assert all(isinstance(company, Company) for company in companies)
    
    @pytest.mark.asyncio
    async def test_get_company_characters(self, stub_client):
        characters = await stub_client.get_company_characters(1)
        assert len(characters) > 0
        assert all(char.company_id == 1 for char in characters)
    
    @pytest.mark.asyncio
    async def test_update_character_level(self, stub_client):
        new_level = 10
        character = await stub_client.update_character_level(1, new_level)
        assert character.level == new_level

class TestAPIClientFactory:
    @pytest.mark.asyncio
    async def test_create_real_client_when_stubs_disabled(self):
        with patch('config.settings.settings.USE_API_STUBS', False):
            client = get_api_client()
            assert isinstance(client, APIClient)
    
    @pytest.mark.asyncio
    async def test_create_stub_client_when_stubs_enabled(self):
        with patch('config.settings.settings.USE_API_STUBS', True):
            client = get_api_client()
            assert isinstance(client, StubAPIClient)