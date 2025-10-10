import asyncio
import random
from typing import List, Optional
from models.models import Company, Character, CharacterDetail, InventoryItem
from utils.logger import get_logger
from config.settings import settings

class StubAPIClient:
    def __init__(self):
        self.logger = get_logger(__name__)
        self._companies = []
        self._characters = []
        self._inventory = {}
        self._init_stub_data()
    
    def _init_stub_data(self):
        """Инициализация тестовых данных"""
        # Компании
        self._companies = [
            Company(id=1, name="🐉 Поход за Слезой Дракона"),
            Company(id=2, name="🏰 Тайны Подземелья"),
            Company(id=3, name="🌌 Звездные Врата"),
        ]
        
        # Персонажи для каждой компании
        self._characters = [
            # Компания 1
            Character(id=1, name="Арагорн", level=5, rating=85, company_id=1),
            Character(id=2, name="Гендальф", level=7, rating=92, company_id=1),
            Character(id=3, name="Леголас", level=6, rating=88, company_id=1),
            
            # Компания 2  
            Character(id=4, name="Траск", level=3, rating=75, company_id=2),
            Character(id=5, name="Элайра", level=4, rating=82, company_id=2),
            
            # Компания 3
            Character(id=6, name="Нова", level=8, rating=95, company_id=3),
        ]
        
        # Инвентарь для персонажей
        self._inventory = {
            1: [
                InventoryItem(id=1, name="Меч Андрила", description="Легендарный меч, светящийся в присутствии орков", quantity=1),
                InventoryItem(id=2, name="Кольцо Духа", description="Увеличивает мудрость на +2", quantity=1),
                InventoryItem(id=3, name="Золотые монеты", description="", quantity=150),
            ],
            2: [
                InventoryItem(id=4, name="Посох Мага", description="Увеличивает силу заклинаний на 20%", quantity=1),
                InventoryItem(id=5, name="Свиток огненного шара", description="", quantity=3),
            ],
            3: [
                InventoryItem(id=6, name="Лук Галадриэли", description="Эльфийский лук невероятной точности", quantity=1),
                InventoryItem(id=7, name="Стрелы", description="", quantity=24),
            ]
        }
    
    async def _simulate_api_call(self):
        """Имитация задержки API"""
        if settings.STUB_DELAY > 0:
            await asyncio.sleep(settings.STUB_DELAY)
    
    async def get_companies(self) -> List[Company]:
        await self._simulate_api_call()
        self.logger.info("STUB: Получение списка компаний")
        return self._companies.copy()
    
    async def get_company_characters(self, company_id: int) -> List[Character]:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Получение персонажей компании {company_id}")
        return [c for c in self._characters if c.company_id == company_id]
    
    async def get_character(self, character_id: int) -> CharacterDetail:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Получение данных персонажа {character_id}")
        
        character = next((c for c in self._characters if c.id == character_id), None)
        if not character:
            raise ValueError(f"Персонаж {character_id} не найден")
        
        inventory = self._inventory.get(character_id, [])
        return CharacterDetail(
            **character.dict(),
            inventory=inventory
        )
    
    async def update_character_level(self, character_id: int, level: int) -> Character:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Обновление уровня персонажа {character_id} на {level}")
        
        character = next((c for c in self._characters if c.id == character_id), None)
        if character:
            character.level = level
        return character
    
    async def update_character_rating(self, character_id: int, rating: int) -> Character:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Обновление рейтинга персонажа {character_id} на {rating}")
        
        character = next((c for c in self._characters if c.id == character_id), None)
        if character:
            character.rating = rating
        return character
    
    async def add_inventory_item(self, character_id: int, item: InventoryItem) -> InventoryItem:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Добавление предмета в инвентарь персонажа {character_id}")
        
        if character_id not in self._inventory:
            self._inventory[character_id] = []
        
        # Генерируем ID для нового предмета
        new_id = max([i.id for i in self._inventory[character_id]] or [0]) + 1
        item.id = new_id
        self._inventory[character_id].append(item)
        
        return item
    
    async def delete_inventory_item(self, item_id: int) -> bool:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Удаление предмета {item_id}")
        
        for character_id, items in self._inventory.items():
            for i, item in enumerate(items):
                if item.id == item_id:
                    del items[i]
                    return True
        return False
    
    async def get_character_jpeg(self, character_id: int) -> bytes:
        await self._simulate_api_call()
        self.logger.info(f"STUB: Генерация JPEG для персонажа {character_id}")
        
        # Создаем простой JPEG с информацией (в реальности здесь была бы генерация изображения)
        # Для примера возвращаем минимальный валидный JPEG
        stub_jpeg = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
            b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\x09\x09\x08'
            b'\x0a\x0c\x14\x0d\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e'
            b'\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xdb\x00C\x01'
            b'\x09\x09\x09\x0c\x0b\x0c\x18\x0d\x0d\x182!\x1c!22222222222222222222222222'
            b'\x222222222222222222222222222222222222\xff\xc0\x00\x11\x08\x00\x01\x00'
            b'\x01\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1f\x00\x00\x01'
            b'\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02'
            b'\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01'
            b'\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01\x02\x03\x00\x04'
            b'\x11\x05\x12!1A\x06\x13Qa\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1'
            b'\xf0$3br\x82\t\n\x16\x17\x18\x19\x1a%&\'()*456789:CDEFGHIJSTUVWXYZcdef'
            b'\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a'
            b'\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9'
            b'\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8'
            b'\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5'
            b'\xf6\xf7\xf8\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00'
            b'?\x00\xfb\xda\x80\x1f\xff\xd9'
        )
        
        return stub_jpeg
    
    async def update_character_rating(self, character_id: int, rating: int) -> Character:
        """Заглушка для обновления рейтинга"""
        await self._simulate_api_call()
        self.logger.info(f"STUB: Обновление рейтинга персонажа {character_id} на {rating}")
        
        character = next((c for c in self._characters if c.id == character_id), None)
        if character:
            character.rating = rating
            return character
        raise ValueError(f"Персонаж {character_id} не найден")