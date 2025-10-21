from pydantic import BaseModel, Field
from typing import List, Optional


class Company(BaseModel):
    id: int
    name: str


class Character(BaseModel):
    id: int
    name: str
    level: int
    rating: int
    company_id: int


class InventoryItem(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    quantity: int = 1


class CharacterDetail(Character):
    inventory: List[InventoryItem] = []


class InventoryItemCreate(BaseModel):
    """Модель для создания предмета"""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    quantity: int = Field(1, ge=1, le=1000)


class InventoryItemUpdate(BaseModel):
    """Модель для обновления предмета"""

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    quantity: Optional[int] = Field(default=None, ge=1, le=1000)
