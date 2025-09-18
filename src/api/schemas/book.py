from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    price: float
    rating: int
    availability: bool
    category: str
    image: Optional[str]

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True
