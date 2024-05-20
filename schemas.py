# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class AddressBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    id: int

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
