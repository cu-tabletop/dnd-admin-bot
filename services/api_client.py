import aiohttp
import logging
from typing import List, Optional
from config.settings import settings
from models.models import Company, Character, CharacterDetail, InventoryItem
from services.stub_api_client import StubAPIClient
from utils.logger import get_logger, log_rating_operations


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.logger = get_logger(__name__)
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            self.logger.error(f"API request failed: {e}")
            raise
    
    async def get_companies(self) -> List[Company]:
        data = await self._make_request("GET", "companies")
        return [Company(**item) for item in data]
    
    async def get_company_characters(self, company_id: int) -> List[Character]:
        data = await self._make_request("GET", f"companies/{company_id}/characters")
        return [Character(**item) for item in data]
    
    async def get_character(self, character_id: int) -> CharacterDetail:
        data = await self._make_request("GET", f"characters/{character_id}")
        return CharacterDetail(**data)
    
    async def update_character_level(self, character_id: int, level: int) -> Character:
        data = await self._make_request("PATCH", f"characters/{character_id}", json={"level": level})
        return Character(**data)
    
    async def update_character_rating(self, character_id: int, rating: int) -> Character:
        data = await self._make_request("PATCH", f"characters/{character_id}", json={"rating": rating})
        return Character(**data)
    
    async def add_inventory_item(self, character_id: int, item: InventoryItem) -> InventoryItem:
        data = await self._make_request("POST", f"characters/{character_id}/inventory", json=item.dict())
        return InventoryItem(**data)
    
    async def delete_inventory_item(self, item_id: int) -> bool:
        await self._make_request("DELETE", f"inventory/{item_id}")
        return True
    
    async def get_character_jpeg(self, character_id: int) -> bytes:
        url = f"{self.base_url}/characters/{character_id}/export/jpeg"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.read()
            
    @log_rating_operations
    async def update_character_rating(self, character_id: int, rating: int) -> Character:
        """Обновление рейтинга персонажа"""
        data = await self._make_request("PATCH", f"characters/{character_id}", json={"rating": rating})
        return Character(**data)
            

def get_api_client():
    if settings.USE_API_STUBS:
        return StubAPIClient()
    else:
        return APIClient()