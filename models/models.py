from pydantic import BaseModel
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
    